# Change: tenant-receipts

Status: Spec reviewed; implementation authorized. Baseline: `../../product/receipts.md` and fixture source. Preserve the baseline while the change is active.

## Motivation and scope

Request IDs can collide between tenants, suppressing jobs and exposing receipts. Scope request IDs to authenticated tenants and reject conflicting payloads. Preserve the handler signature and ordinary success response. Affected behavior: R-01. No archive or publication is authorized in this trial.
