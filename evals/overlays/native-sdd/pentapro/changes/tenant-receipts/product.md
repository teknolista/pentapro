# PRODUCT

Baseline: `../../product/receipts.md`. Preserve S-01 while changing R-01.

## Modify R-01

### Requirement R-01: Receipt retries

The handler SHALL preserve its signature and scope valid request IDs to the authenticated tenant. It SHALL return HTTP 202 and a receipt for new requests and exact replays, with at most one job per tenant and ID. Conflicting payloads SHALL return HTTP 409 with `{"error": "idempotency_conflict"}` and preserve state. Missing identity SHALL return HTTP 401 and malformed input HTTP 400, without creating jobs.

#### Scenario S-02: Independent tenants use the same ID

- **WHEN** two authenticated tenants submit valid requests with the same ID
- **THEN** each receives HTTP 202 and its own receipt, and each creates one job

#### Scenario S-01: Request ID is replayed

- **WHEN** a tenant repeats the same ID and payload
- **THEN** it receives HTTP 202 and its original receipt without creating another job

#### Scenario S-03: Conflicting replay

- **WHEN** a tenant repeats the ID with a different payload
- **THEN** it receives the specified conflict response and the original receipt and job remain unchanged

#### Scenario S-04: Rejected calls have no effect

- **WHEN** a request is unauthenticated or malformed
- **THEN** it returns the corresponding error and creates no job
