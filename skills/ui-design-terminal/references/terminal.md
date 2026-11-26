# Terminal interaction and evidence

## Establish the output contract

Identify command, user task, platform, shell, terminal capabilities and actual data contracts. Inspect existing flags, exit codes, stdout/stderr and compatibility promises. A non-interactive invocation may run in a CI job, a pipe or a file. Choose output by explicit mode and TTY capabilities: machine-readable formats must contain only the documented data, preserve schema and exit semantics, avoid color/control sequences and keep diagnostics on stderr. Redirected human output should remain legible without cursor updates or escape codes. Do not assume every TTY supports color, Unicode, mouse or a fixed width; honor existing no-color and output options. Never change a stable script-facing format silently.

## Compose for a real viewport

Group related information around the task; use headings and labels only where useful. Align comparable columns and numeric values, include units and distinguish zero, missing, unknown and stale. Try realistic long labels, wide numbers, Unicode and narrow widths. Wrap, truncate or offer details deliberately; keep essential information accessible. For TUI selection, inspect the actual visible rows, scroll position, selected item's identity and detail panel together: a valid selection index is not evidence that the item or its chart is rendered. Define focus and selected versus inactive cues without relying on color alone.

Use a representative task and real target dimensions early. Resize narrower and wider during interaction; preserve or deliberately reconcile selection, scrolling and focus, and ensure the selected content remains visible. Avoid overlapping regions, broken borders and hidden recovery controls. Account for terminal cell widths rather than string length alone when relevant. Provide discoverable keyboard navigation, action labels and context-sensitive help; ensure an alternative to mouse-only or color-only controls. Respect the existing application's interaction conventions.

## Progress, failure and recovery

For long or multi-pass work, label phase and current progress in truthful units where known; do not imply a total or completion percentage when unknown. Ensure phase changes and final summary remain understandable, including in redirected output. Make cancellation behavior explicit: how to stop, what partial effects remain, and whether resumption or retry is supported by the real contract. Errors should identify the affected operation and a feasible next action without exposing secrets. Distinguish failure from empty output, partial success, pending work and unknown outcome. Preserve context needed to recover; never promise rollback, idempotency or retry safety without evidence. Define meaningful exit status for non-interactive callers.

## Observe the journey

For an authorized implementation, use the existing test and build tools and a controlled fixture. Exercise an early vertical slice in a real PTY at a recorded width and height: enter the command, navigate to a representative item, confirm the selected row and associated content are visibly rendered, perform the primary action and inspect the resulting state. Exercise resize, keyboard help and a relevant failure or cancellation path. If the task changes redirects or structured output, separately check stdout, stderr, exit status, absence of terminal controls and schema with a pipe or file. Do not send consequential commands to a live service without authorization; leave a specific pending check if safe fixtures or a PTY are unavailable.

Capture target revision, command, fixture, terminal size, actions and observed output. A screenshot or PTY capture shows rendered presentation, not durable task success: verify the outcome via the supported read-back or state contract. A state/unit test or selection value does not prove that the selected content is in the viewport. Record what ran, failures, untested combinations and limitations; do not claim accessibility or user validation from a capture alone.
