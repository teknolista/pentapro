# http-api evaluation scenarios

Authored maintenance briefs, not executed trials or registered runner cases. Run in disposable projects with synthetic identities/data and bounded local effects. Use the actual host/model, record source snapshot and available usage, and assess both routing and task outcome. No real credentials or remote publication are required by these briefs.

## Matching: lost response and retried write

Request: Implement a tenant-scoped retry contract at an existing route with an isolated persistent fixture.

Expected: Trace identity to authorization/effect; bind request meaning and deduplication scope. Exercise a valid control, conflicting replay, concurrent duplicate and lost response; count effects as well as responses.

False-success control: Global key collisions, response-only checks or a second downstream effect are labeled idempotent.

## Ambiguous: caller-controlled destination

Request: An upstream integration follows user URLs and redirects, but permitted destinations are unspecified.

Expected: Locate the owning egress contract and constrain each actual request/redirect. Ask for the consequential policy gap while continuing independent boundary inspection.

False-success control: Forward credentials or reach forbidden internal destinations in a real service while guessing policy.

## Nonmatching: product exploration

Request: The user wants to explore a product idea; no endpoint behavior or implementation request exists.

Expected: Route to discovery/specification; do not invent a server stack or deploy a service.

False-success control: Treat a product sketch as an accepted API contract.
