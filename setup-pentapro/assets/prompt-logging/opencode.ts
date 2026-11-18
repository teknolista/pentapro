/**
 * OpenCode project adapter for the shared prompt-log core.
 *
 * Place it at `.opencode/plugins/agents-log.ts` for project auto-discovery.
 *
 * The plugin id is distinct from the personal `agents-log` plugin so both can
 * be loaded. The adapter sets a process flag at setup; a personal global
 * plugin should check that flag before logging so a project hook never
 * produces duplicate entries.
 */

import { Plugin } from "@opencode/plugin"
import { join } from "node:path"
import {
	appendEntry,
	formatEntry,
	isUserPrompt,
	messageText,
} from "../../scripts/agents-log/core.mjs"

declare global {
	var __agentsLogProjectCapture: boolean | undefined
}

export default Plugin.define({
	id: "agents-log-project",
	async setup(ctx) {
		const root = ctx.location.project?.directory
		if (!root) throw new Error("[agents-log] OpenCode did not provide the project root")
		const logPath = join(root, "AGENTS.log")
		const seen = new Set()

		// Read by a personal global capture, which must yield to the project.
		globalThis.__agentsLogProjectCapture = true

		await ctx.session.hook("context", (event) => {
			const messages = Array.isArray(event?.messages) ? event.messages : []

			for (const message of messages) {
				if (!isUserPrompt(message) || seen.has(message.id)) continue

				const model = event?.model ?? {}
				const entry = formatEntry({
					text: messageText(message),
					host: "opencode",
					provider: model.providerID,
					model: model.id ?? model.modelID,
					variant: model.variant,
					agent: event?.agent,
				})

				try {
					appendEntry(logPath, entry)
				} catch (error) {
					const detail = error instanceof Error ? error.message : String(error)
					console.error(`[agents-log] failed to append to ${logPath}: ${detail}`)
					// A prompt must never reach the model unlogged.
					throw new Error(`[agents-log] failed to write ${logPath}: ${detail}`)
				}

				seen.add(message.id)
			}
		})
	},
})
