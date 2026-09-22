# awc-013-duplicate-action-id

**Verdict:** `INVALID_INPUT` (AWC preflight)

**Story:** Reference trace reuses the same `action_id` on two different tool hops. A witness ledger must be injective per session anchor.

**Fact check:** WitnessDiff `compare_witness_integrity` alone yields `WITNESS_OMISSION` for this pair. AWC v0.1 normatively rejects duplicate anchors in preflight before compare.
