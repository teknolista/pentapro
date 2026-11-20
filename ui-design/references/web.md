# Web screens

Inspect the actual HTML/CSS/framework, routes, components and supported browser range. Preserve the stack and component library. A design task does not require React, Tailwind, a CSS reset or an animation dependency.

## Layout and navigation

Use semantic document structure, headings and landmarks that match content. Use links for navigation and buttons for actions; native controls before custom widgets. Follow the component library's accessible patterns, checking its configured behavior rather than assuming a library ensures accessibility.

Make layout respond to available content/container width, not only device labels. Document meaningful transitions: column collapse, navigation changes, table scrolling/alternative presentation, reading width and control placement. Test a narrow viewport, larger views and widths near actual transitions, plus long content and zoom. Avoid unintended page-wide overflow and clipped focus; intentional data-table scrolling needs clear, accessible access. Keep browser zoom available. Account for dynamic viewport height, safe areas, virtual keyboard and sticky content that can obscure controls.

Specify route, URL state for shareable filters when appropriate, direct entry, browser Back/Forward, scroll/focus restoration and unsaved-data handling. Link activation and form submission should work with expected browser conventions. Do not hijack shortcuts or replace native scrolling for decoration.

## Accessibility and input

Use the project's specified accessibility target; propose WCAG 2.2 AA for web when none is defined and record it as a proposal. Relevant numerical criteria include normal text contrast 4.5:1, qualifying large text 3:1, and applicable non-text UI contrast 3:1. Criterion definitions and exceptions matter: do not treat every decorative boundary as required contrast. WCAG 2.2 AA target-size minimum is 24 by 24 CSS px with defined exceptions/spacing alternatives; a larger project touch target is a usability choice, not the same criterion. Android uses dp and a separate platform baseline.

Check accessible name/role/state, visible labels matching spoken names, logical reading/focus order, visible unobscured focus and all essential keyboard interactions. Avoid positive tabindex as a focus-order repair. For modal dialogs, move focus appropriately inside, contain keyboard interaction, make the background inert, support appropriate dismissal and restore focus to a valid place. An ARIA attribute alone does not implement behavior. For custom widgets use the relevant WAI-ARIA APG pattern and test it.

Provide text alternatives, caption/transcript support where applicable, clear errors and relevant status announcements. Support reduced motion, zoom/reflow and text spacing. Give drag or complex gesture operations a simple alternative. Avoid memory/puzzle-only authentication barriers where the selected standard requires alternatives. Automated checks cannot establish complete conformance or real screen-reader usability.

## Implementation and checks

Model remote state separately from local editing, keep stable item identity and account for races, cancellation, stale data and pending mutations. Reserve media space and load assets proportionately; virtualize large collections only with keyboard/search/assistive behavior considered. Address demonstrated performance bottlenecks before speculative memoization.

For a slow browser route, trace the requests that delay the first usable state. Check which requests can start independently and which wait for identity, permissions, or prior results. Keep those dependencies and bound concurrency. Verify the changed timing and relevant partial-failure states on a comparable run.

Render untrusted content as text through the framework's supported escaping path. If actual rich HTML is required, use the project's reviewed sanitization policy and safe rendering integration; do not enable raw HTML insertion just to reproduce a mock. Treat destination URLs separately from display text and validate supported schemes according to the actual use. Output escaping, sanitization and URL handling address different contexts. See [MDN's XSS guidance](https://developer.mozilla.org/en-US/docs/Web/Security/Attacks/XSS).

Use existing project build/lint/type/component/browser checks appropriate to the change. Drive actual controls and navigation with representative data; inspect console/network failures without exposing secrets. A DOM value assignment or direct event-handler call does not prove the keyboard/pointer interaction works. Use browser screenshot/DOM/accessibility-tree evidence together; do not infer screen-reader output from the tree alone.

Primary references: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/), [modal dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [responsive design](https://web.dev/learn/design). Verify version-sensitive framework APIs against official documentation when implementing.

## Composition input and forced colors

For a custom Enter shortcut that sends, searches or clears input, distinguish IME character confirmation from submission. An Enter confirming composition must preserve the text without triggering the action; a separate submission must occur only once. Preserve the contract for Shift+Enter and other modifiers, paste, explicit submit controls and native validation. Use supported composition events and verify browser/OS/input-method behavior, including relevant Japanese, Chinese or Korean input; do not install a universal legacy key-code workaround or replace native form behavior unnecessarily. [UI Events](https://www.w3.org/TR/uievents/#events-composition-key-events) · [IME research](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/2de1134dc4d1cfe112934611ae5803ae17a1bd7e/docs/ime-composition.md)

For web accessibility work on supported targets, inspect focus, boundaries, icons and selected/error states with forced colors enabled. Shadows or background colors may disappear, so preserve meaningful cues through native semantics, system colors and appropriate borders/outlines. Prefer targeted repairs over disabling the user's forced colors or creating a separate design. Record the actual browser/OS mode exercised; emulation alone does not establish all platform behavior. [Forced colors](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/forced-colors)
