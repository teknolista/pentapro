# Receipts

## Purpose

Accept job requests and return a receipt through the service handler.

## Requirements

### Requirement R-01: Receipt retries

The service SHALL return HTTP 202 with a receipt for a valid authenticated request. Repeating a request ID returns its existing receipt.

#### Scenario S-01: Request ID is replayed

- **WHEN** a valid authenticated request repeats an existing request ID
- **THEN** the service returns the existing receipt without creating another job
