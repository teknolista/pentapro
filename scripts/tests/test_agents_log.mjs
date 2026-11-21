import assert from "node:assert/strict"
import {
	existsSync,
	linkSync,
	readFileSync,
	rmSync,
	statSync,
	symlinkSync,
	writeFileSync,
	mkdtempSync,
} from "node:fs"
import { tmpdir } from "node:os"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"
import { spawnSync } from "node:child_process"
import { after, test } from "node:test"

import {
	appendEntry,
	extractPrompt,
	formatEntry,
	isUserPrompt,
	messageText,
	normalizePayload,
	redact,
	resolveLogPath,
	rfc5322,
} from "../../setup-pentapro/assets/prompt-logging/core.mjs"

const here = dirname(fileURLToPath(import.meta.url))
const cli = join(here, "..", "..", "setup-pentapro", "assets", "prompt-logging", "log-prompt.mjs")
const temporary = []

function temporaryDirectory() {
	const directory = mkdtempSync(join(tmpdir(), "agents-log-"))
	temporary.push(directory)
	return directory
}

after(() => {
	for (const directory of temporary) rmSync(directory, { recursive: true, force: true })
})

test("rfc5322 uses the documented shape and local offset", () => {
	const value = rfc5322(new Date(2026, 10, 18, 9, 14, 5))
	assert.match(value, /^[A-Z][a-z]{2}, 18 Nov 2026 09:14:05 [+-]\d{4}$/)
})

test("redact covers the documented credential patterns", () => {
	assert.equal(redact("sk-1234567890abcdef"), "[REDACTED api key]")
	assert.equal(redact("senha: hunter2"), "senha: [REDACTED]")
	assert.equal(redact("Authorization: Bearer abcdefghijklmnop"), "Authorization: Bearer [REDACTED]")
	assert.equal(
		redact("-----BEGIN RSA PRIVATE KEY-----\nsecret\n-----END RSA PRIVATE KEY-----"),
		"[REDACTED private key]",
	)
	assert.equal(
		redact("eyJabcdefgh.abcdefgh.abcdefgh"),
		"[REDACTED jwt]",
	)
	assert.equal(redact("plain prompt"), "plain prompt")
})

test("extractPrompt handles every documented host payload", () => {
	for (const payload of [
		{ prompt: "claude" },
		{ prompt: "codex", model: "gpt-6.1" },
		{ prompt: "cursor", model: "claude-opus", model_id: "claude-opus-4" },
		{ prompt: "copilot" },
	]) {
		assert.equal(extractPrompt(payload).text, payload.prompt)
	}
	assert.deepEqual(
		extractPrompt({ prompt: "with files", attachments: [{ file_path: "/tmp/a.txt" }] }).attachments,
		["/tmp/a.txt"],
	)
	assert.equal(extractPrompt({ user_prompt: "alias" }).text, "alias")
	assert.equal(extractPrompt({ prompt: "" }).text, "")
	assert.throws(() => extractPrompt({}), /no prompt field/)
})

test("normalizePayload accepts string and object model shapes", () => {
	const stringModel = normalizePayload(
		{ prompt: "x", model: "gpt-6.1", agent_type: "reviewer" },
		{ host: "codex" },
	)
	assert.equal(stringModel.host, "codex")
	assert.equal(stringModel.model, "gpt-6.1")
	assert.equal(stringModel.agent, "reviewer")

	const objectModel = normalizePayload(
		{ prompt: "x", model: { providerID: "openrouter", id: "deepseek", variant: "high" }, agent: "build" },
		{ host: "opencode" },
	)
	assert.equal(objectModel.provider, "openrouter")
	assert.equal(objectModel.model, "deepseek")
	assert.equal(objectModel.variant, "high")
	assert.equal(objectModel.agent, "build")

	const cursor = normalizePayload({ prompt: "x", model: "cursor-model", model_id: "cursor-model" }, {
		host: "cursor",
	})
	assert.equal(cursor.model, "cursor-model")
})

test("formatEntry keeps the prompt verbatim and adds host metadata only when useful", () => {
	const date = new Date(2026, 10, 18, 9, 14, 5)

	const sameProvider = formatEntry({
		text: "line one\nline two",
		date,
		host: "opencode",
		provider: "opencode",
		model: "deepseek",
		agent: "build",
	})
	assert.match(
		sameProvider,
		/^## [A-Z][a-z]{2}, 18 Nov 2026 09:14:05 [+-]\d{4} \| opencode\/deepseek \(agent build\)\nline one\nline two\n\n$/,
	)

	const otherProvider = formatEntry({
		text: "hello",
		date,
		host: "opencode",
		provider: "openrouter",
		model: "particle",
		agent: "build",
	})
	assert.match(otherProvider, /\| openrouter\/particle \(agent build, host opencode\)\nhello\n\n$/)

	const noModel = formatEntry({ text: "hello", date, host: "claude-code" })
	assert.match(noModel, /\| claude-code\/unknown\nhello\n\n$/)

	const withAttachment = formatEntry({
		text: "hello",
		date,
		host: "cursor",
		attachments: ["/tmp/a.txt"],
	})
	assert.match(withAttachment, /hello\n\n\[attachment: \/tmp\/a.txt\]\n\n$/)
})

test("isUserPrompt excludes harness-injected messages", () => {
	const prompt = {
		role: "user",
		id: "m1",
		metadata: {},
		content: [{ type: "text", text: "a real prompt" }],
	}
	assert.equal(isUserPrompt(prompt), true)
	assert.equal(isUserPrompt({ ...prompt, id: "m2", metadata: { displayText: "x" } }), true)
	assert.equal(isUserPrompt({ ...prompt, metadata: { keepID: "x" } }), false)
	assert.equal(isUserPrompt({ ...prompt, metadata: { recent: true } }), false)
	assert.equal(isUserPrompt({ ...prompt, metadata: undefined }), false)
	assert.equal(isUserPrompt({ ...prompt, role: "assistant" }), false)
	assert.equal(
		isUserPrompt({ ...prompt, content: [{ type: "text", text: "<system-reminder>hide</system-reminder>" }] }),
		false,
	)
})

test("messageText preserves text and marks attachments", () => {
	assert.equal(
		messageText({
			content: [
				{ type: "text", text: "first" },
				{ type: "file", filename: "notes.txt" },
				{ type: "text", text: "second" },
			],
		}),
		"first\n\n[attachment: notes.txt]\n\nsecond",
	)
})

test("appendEntry writes one owner-only file and appends", () => {
	const directory = temporaryDirectory()
	const logPath = resolveLogPath(directory)
	appendEntry(logPath, "first\n\n")
	appendEntry(logPath, "second\n\n")
	assert.equal(readFileSync(logPath, "utf8"), "first\n\nsecond\n\n")
	if (process.platform !== "win32") {
		assert.equal(statSync(logPath).mode & 0o777, 0o600)
	}
})

test("appendEntry reports an unwritable path", () => {
	const directory = temporaryDirectory()
	const parent = join(directory, "not-a-directory")
	writeFileSync(parent, "file")
	assert.throws(() => appendEntry(join(parent, "AGENTS.log"), "entry\n\n"))
})

test("appendEntry refuses a symlink log path", { skip: process.platform === "win32" }, () => {
	const directory = temporaryDirectory()
	const target = join(directory, "outside.log")
	const logPath = resolveLogPath(directory)
	writeFileSync(target, "untouched")
	symlinkSync(target, logPath)
	assert.throws(() => appendEntry(logPath, "prompt\n\n"))
	assert.equal(readFileSync(target, "utf8"), "untouched")
})

test("appendEntry refuses a hard-linked log path", { skip: process.platform === "win32" }, () => {
	const directory = temporaryDirectory()
	const target = join(directory, "outside.log")
	const logPath = resolveLogPath(directory)
	writeFileSync(target, "untouched")
	linkSync(target, logPath)
	assert.throws(() => appendEntry(logPath, "prompt\n\n"), /unlinked file/)
	assert.equal(readFileSync(target, "utf8"), "untouched")
})

test("resolveLogPath rejects a missing root", () => {
	assert.throws(() => resolveLogPath(""))
})

test("CLI appends a hook payload and stays silent", () => {
	const directory = temporaryDirectory()
	const result = spawnSync(process.execPath, [cli, "--host", "codex", "--root", directory], {
		input: JSON.stringify({ prompt: "from hook", model: "gpt-6.1" }),
		encoding: "utf8",
	})
	assert.equal(result.status, 0, result.stderr)
	assert.equal(result.stdout, "")
	assert.equal(result.stderr, "")
	const entry = readFileSync(join(directory, "AGENTS.log"), "utf8")
	assert.match(entry, /\| codex\/gpt-6\.1\nfrom hook\n\n$/)
})

test("CLI records Cursor attachments and redacts credentials", () => {
	const directory = temporaryDirectory()
	const result = spawnSync(process.execPath, [cli, "--host", "cursor", "--root", directory], {
		input: JSON.stringify({
			prompt: "senha: hunter2",
			attachments: [{ file_path: "/tmp/a.txt" }],
		}),
		encoding: "utf8",
	})
	assert.equal(result.status, 0, result.stderr)
	const entry = readFileSync(join(directory, "AGENTS.log"), "utf8")
	assert.match(entry, /senha: \[REDACTED\]/)
	assert.match(entry, /\[attachment: \/tmp\/a\.txt\]/)
})

test("CLI exits 2 on an invalid payload so the host can block", () => {
	const directory = temporaryDirectory()
	const invalid = spawnSync(process.execPath, [cli, "--root", directory], {
		input: "not json",
		encoding: "utf8",
	})
	assert.equal(invalid.status, 2)
	assert.match(invalid.stderr, /invalid JSON/)

	const empty = spawnSync(process.execPath, [cli, "--root", directory], {
		input: "",
		encoding: "utf8",
	})
	assert.equal(empty.status, 2)
	assert.match(empty.stderr, /no hook payload/)

	const missingPrompt = spawnSync(process.execPath, [cli, "--root", directory], {
		input: JSON.stringify({ model: "gpt-6.1" }),
		encoding: "utf8",
	})
	assert.equal(missingPrompt.status, 2)
	assert.match(missingPrompt.stderr, /no prompt field/)
	assert.equal(existsSync(join(directory, "AGENTS.log")), false)

	const fileAsRoot = join(directory, "file")
	writeFileSync(fileAsRoot, "x")
	const unwritable = spawnSync(process.execPath, [cli, "--root", fileAsRoot], {
		input: JSON.stringify({ prompt: "x" }),
		encoding: "utf8",
	})
	assert.equal(unwritable.status, 2)
	assert.match(unwritable.stderr, /\[agents-log\]/)
})

test("attachment labels receive the same credential redaction as prompt text", () => {
 const entry = formatEntry({ text: "synthetic attachment", attachments: ["/tmp/sk-1234567890abcdef.txt"] })
 assert.ok(!entry.includes("sk-1234567890abcdef"))
 assert.match(entry, /attachment: \/tmp\/\[REDACTED api key\]\.txt/)
})
