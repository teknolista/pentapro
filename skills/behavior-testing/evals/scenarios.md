# Numeric boundary evaluation scenarios

Authored maintenance briefs, not executed model trials. Use synthetic fixtures and the project's existing runner.

| Request | Expected behavior | Failure control |
| --- | --- | --- |
| Regress a currency adapter that rejects valid decimal cells and formats an accepted large average as negative | Establish units/range/rounding; exercise real parsing, calculation and public formatting with independent expected values and valid controls | Arithmetic-only checks miss adapter rejection or narrowing at formatting |
| Add fractional averages, but the contract omits rounding and accepted magnitude | Identify the consequential decision; retain safe independent work and report the unresolved acceptance | Copy current output into expected values or invent rounding policy |
| Test a text-only label rename | Select affected label behavior proportionately | Add an unrelated money or overflow suite |

Where the defect is already fixed, retain its current source and label any baseline/fault-sensitivity evidence accurately. These briefs do not demonstrate TDD or model compliance.
