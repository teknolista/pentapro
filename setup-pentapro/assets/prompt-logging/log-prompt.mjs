#!/usr/bin/env node
/**
 * Command-line adapter for host hooks that send JSON on stdin.
 *
 * Usage:
 *   node scripts/agents-log/log-prompt.mjs --host <name> --root <repo> [options]
 *
 * Options: --host, --root, --file, --agent, --provider, --model, --variant.
 * The host configuration examples live in `hosts.md` in this folder.
 *
 * Silence is part of the contract: a successful run writes nothing to stdout
 * or stderr. A failure writes the reason to stderr and exits 2, which blocks
 * the prompt in Claude Code, Codex and Cursor. Copilot reports the failure but
 * cannot block; its instruction rule remains the enforcement layer.
 */

import {
	appendEntry,
	formatEntry,
	normalizePayload,
	resolveLogPath,
} from "./core.mjs"
import { resolve } from "node:path"

function parseArgs(argv) {
	const options = {
		host: "agent",
		root: process.cwd(),
		file: "AGENTS.log",
	}

	for (let index = 0; index < argv.length; index += 1) {
		const argument = argv[index]
		const equals = argument.indexOf("=")
		const flag = equals === -1 ? argument : argument.slice(0, equals)
		const inline = equals === -1 ? undefined : argument.slice(equals + 1)
		const value = () => {
			const result = inline ?? argv[++index]
			if (result === undefined || result === "") {
				throw new Error(`missing value for ${flag}`)
			}
			return result
		}

		switch (flag) {
			case "--host":
				options.host = value()
				break
			case "--root":
				options.root = value()
				break
			case "--file":
				options.file = value()
				break
			case "--agent":
				options.agent = value()
				break
			case "--provider":
				options.provider = value()
				break
			case "--model":
				options.model = value()
				break
			case "--variant":
				options.variant = value()
				break
			default:
				throw new Error(`unknown option ${flag}`)
		}
	}

	options.root = resolve(options.root)
	return options
}

async function readStdin() {
	const chunks = []
	for await (const chunk of process.stdin) chunks.push(chunk)
	return Buffer.concat(chunks).toString("utf8")
}

async function main() {
	const options = parseArgs(process.argv.slice(2))
	const input = (await readStdin()).trim()

	if (!input) {
		throw new Error("no hook payload on stdin")
	}

	let payload
	try {
		payload = JSON.parse(input)
	} catch (error) {
		throw new Error(`invalid JSON on stdin: ${error instanceof Error ? error.message : String(error)}`)
	}

	const entry = formatEntry(normalizePayload(payload, options))
	const logPath = resolveLogPath(options.root, options.file)
	appendEntry(logPath, entry)
}

main().catch((error) => {
	const detail = error instanceof Error ? error.message : String(error)
	console.error(`[agents-log] ${detail}`)
	process.exit(2)
})
