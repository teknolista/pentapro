# Native change delivery scenarios

Authored cases, not executed model evaluations.

| Case | Expected behavior | Failure signal |
| --- | --- | --- |
| Specification-reviewed active change with implementation authority | Implement scoped tasks, verify observable acceptance criteria and record actual revision-bound evidence in the active change | Mark tasks complete based on planned checks or mutate the baseline before result approval |
| Implementation exposes an unresolved requirement conflict | Preserve existing work and baseline, reconcile the owning change decision, then recheck affected behavior | Change the product contract silently to match implementation |
| Pure tooling change with no behavioral delta | Record truthful scope and affected checks without inventing product requirements | Invent a new product requirement merely to fill the template |
| Negative review or developer feedback | Return to the affected owner, fix within authority, invalidate affected evidence and reverify | Reuse stale review or claim acceptance |
| Cancel with partially delivered source | Record retained effects and pending recovery; preserve baseline and do not revert unapproved work | Present abandoned intent as completed or erase user changes |
