/**
 * Shared prompt-log core.
 *
 * One implementation of the entry format, redaction and append contract for
 * every supported coding agent. The OpenCode plugin imports these functions
 * directly; the command-line adapter reads the host hook payload from stdin
 * and calls them. Keep this file dependency-free so a project can copy it
 * without a package manager, network access or build step.
 */

import {
	constants,
	closeSync,
	fstatSync,
	lstatSync,
	openSync,
	writeFileSync,
} from "node:fs"
import { join } from "node:path"

const LOG_FILE = "AGENTS.log"

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

const REDACTIONS = [
	[
		/-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----/g,
		"[REDACTED private key]",
	],
	[/\b(?:sk|rk|pk)-[A-Za-z0-9_-]{16,}\b/g, "[REDACTED api key]"],
	[/\b(?:gh[pousr]|github_pat)_[A-Za-z0-9_]{16,}\b/g, "[REDACTED token]"],
	[/\bAKIA[0-9A-Z]{16}\b/g, "[REDACTED access key]"],
	[/\bAIza[0-9A-Za-z_-]{30,}\b/g, "[REDACTED api key]"],
	[/\bxox[abprs]-[A-Za-z0-9-]{10,}\b/g, "[REDACTED token]"],
	[/\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b/g, "[REDACTED jwt]"],
	[
		/(\b(?:password|passwd|senha|token|secret|api[_-]?key)\b\s*[:=]\s*)\S+/gi,
		"$1[REDACTED]",
	],
	[/(\bBearer\s+)[A-Za-z0-9._~+/=-]{12,}/gi, "$1[REDACTED]"],
]

const pad = (value) => String(value).padStart(2, "0")

/** RFC 5322 date-time in local time, e.g. `Tue, 17 Nov 2026 13:30:45 -0300`. */
export function rfc5322(date) {
	const offset = -date.getTimezoneOffset()
	const sign = offset < 0 ? "-" : "+"
	const absolute = Math.abs(offset)
	const zone = `${sign}${pad(Math.floor(absolute / 60))}${pad(absolute % 60)}`
	return (
		`${DAYS[date.getDay()]}, ${pad(date.getDate())} ${MONTHS[date.getMonth()]} ` +
		`${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}:` +
		`${pad(date.getSeconds())} ${zone}`
	)
}

/** Best-effort removal of credentials; the instruction layer still forbids pasting them. */
export function redact(text) {
	return REDACTIONS.reduce(
		(current, [pattern, replacement]) => current.replace(pattern, replacement),
		text,
	)
}

/** Flattens an OpenCode message's content into the text that was sent. */
export function messageText(message) {
	const parts = Array.isArray(message?.content) ? message.content : []
	const chunks = []
	for (const part of parts) {
		if (part?.type === "text" && typeof part.text === "string") {
			chunks.push(part.text)
		} else if (part?.type === "file") {
			chunks.push(`[attachment: ${part.filename ?? part.url ?? "unnamed"}]`)
		}
	}
	return chunks.join("\n\n")
}

/**
 * OpenCode stores harness-injected context with the `user` role. Real prompts
 * carry either empty metadata (CLI `run`) or a `displayText` field, while the
 * conversation checkpoint carries `keepID`/`recent` and the plan-mode reminder
 * carries no metadata at all. The markup guard is a second line of defence.
 */
export function isUserPrompt(message) {
	if (message?.role !== "user" || !message?.id) return false
	const metadata = message.metadata
	if (!metadata || typeof metadata !== "object") return false
	if ("keepID" in metadata || "recent" in metadata) return false
	return !/^\s*<(?:system-reminder|context|environment_context|conversation-checkpoint)>/i.test(
		messageText(message),
	)
}

/**
 * Extracts the prompt and attachment names from a stdin hook payload.
 * Claude Code, Codex, Cursor and Copilot all send `prompt`; the other keys are
 * accepted so a host that renames the field fails explicitly rather than
 * silently recording an empty prompt.
 */
export function extractPrompt(payload) {
	if (!payload || typeof payload !== "object") {
		throw new Error("hook payload must be an object")
	}

	let text = ""
	let hasPrompt = false
	for (const key of ["prompt", "user_prompt", "userPrompt", "message", "text"]) {
		if (typeof payload[key] === "string") {
			text = payload[key]
			hasPrompt = true
			break
		}
	}
	if (!hasPrompt) throw new Error("hook payload has no prompt field")

	const attachments = []
	if (Array.isArray(payload.attachments)) {
		for (const attachment of payload.attachments) {
			const name = attachment?.file_path ?? attachment?.path ?? attachment?.name
			if (name) attachments.push(String(name))
		}
	}

	return { text, attachments }
}

/**
 * Normalizes host-specific fields into the values used by `formatEntry`.
 * `model` is a string in Codex/Cursor and an object in OpenCode; both shapes
 * are accepted so the same core can serve every adapter.
 */
export function normalizePayload(payload, options = {}) {
	const { text, attachments } = extractPrompt(payload)
	const modelValue = payload?.model
	const modelObject = modelValue && typeof modelValue === "object" ? modelValue : undefined

	const host = options.host || payload?.host || "agent"
	const provider =
		options.provider ||
		payload?.provider ||
		modelObject?.providerID ||
		modelObject?.provider
	const model =
		options.model ||
		(typeof modelValue === "string" ? modelValue : undefined) ||
		modelObject?.id ||
		modelObject?.modelID ||
		modelObject?.model ||
		payload?.model_id ||
		payload?.modelId
	const variant = options.variant || modelObject?.variant
	const agent =
		options.agent ||
		payload?.agent ||
		payload?.agent_type ||
		payload?.agentType

	return { text, attachments, host, provider, model, variant, agent }
}

/** `provider/model` when known, otherwise the host with an explicit unknown model. */
function attribution({ host, provider, model, variant }) {
	const source =
		provider && provider !== host ? `${provider}/${model || "unknown"}` : `${host || "agent"}/${model || "unknown"}`
	return `${source}${variant && variant !== "default" ? `#${variant}` : ""}`
}

/**
 * Builds one append-only entry. The body is the prompt verbatim after
 * redaction; attachments follow it as `[attachment: <name>]`.
 */
export function formatEntry({
	text,
	date = new Date(),
	host = "agent",
	provider,
	model,
	variant,
	agent,
	attachments = [],
}) {
	const meta = []
	if (agent) meta.push(`agent ${agent}`)
	if (provider && host && host !== provider) meta.push(`host ${host}`)
	const metaText = meta.length > 0 ? ` (${meta.join(", ")})` : ""

	const bodyParts = [redact(text || "[empty prompt]")]
	for (const attachment of attachments) bodyParts.push(`[attachment: ${redact(String(attachment))}]`)

	return `## ${rfc5322(date)} | ${attribution({ host, provider, model, variant })}${metaText}\n${bodyParts.join("\n\n")}\n\n`
}

/** Appends synchronously without following a symlink; new files are owner-only. */
export function appendEntry(logPath, entry) {
	try {
		if (!lstatSync(logPath).isFile()) {
			throw new Error("log path must be a regular file")
		}
	} catch (error) {
		if (error?.code !== "ENOENT") throw error
	}

	const flags =
		constants.O_WRONLY |
		constants.O_APPEND |
		constants.O_CREAT |
		(constants.O_NONBLOCK ?? 0) |
		(constants.O_NOFOLLOW ?? 0)
	const fileDescriptor = openSync(logPath, flags, 0o600)
	try {
		const file = fstatSync(fileDescriptor)
		if (!file.isFile() || file.nlink !== 1) {
			throw new Error("log path must be a regular, unlinked file")
		}
		writeFileSync(fileDescriptor, entry, { encoding: "utf8" })
	} finally {
		closeSync(fileDescriptor)
	}
}

/** Resolves the log path; the caller is responsible for the repository root. */
export function resolveLogPath(root, fileName = LOG_FILE) {
	if (!root) throw new Error("a repository root is required")
	return join(root, fileName)
}
