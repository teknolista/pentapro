# PROJECT

## Context and decision

The existing handler supplies the principal. Scope receipt lookup by authenticated tenant and request ID; retain the payload and receipt to distinguish exact replays from conflicts. Preserve input and identity rejection behavior. The alternative of global request IDs can leak or suppress another tenant's receipt.

## Risks and alternatives

The fixture exercises sequential calls in memory. A persistent or concurrent deployment needs separate transaction and failure-path validation.
