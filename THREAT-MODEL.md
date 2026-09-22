# Threat model (exporter-centric)

AWC v0.1 fixtures model **honest-but-hazardous exporter failures**, not nation-state attackers.

| Failure mode | Example fixture | Verdict |
|--------------|-----------------|---------|
| Silent hop drop under complete claim | `awc-002-silent-omission` | `COMPLETENESS_OVERCLAIM` |
| Marketing count ≠ attested hops | `awc-003-declared-count-overclaim` | `COMPLETENESS_OVERCLAIM` |
| Honest partial export | `awc-004-partial-path-omission` | `WITNESS_OMISSION` |
| Truncated tail | `awc-005-truncated-tail-omission` | `WITNESS_OMISSION` |
| Invented hop | `awc-006-extra-hop-in-export`, `awc-007-fabricated-export-hop` | `EXPORT_TRUNCATION` |
| Order / binding drift | `awc-008`–`awc-010`, `awc-014` | `MISMATCH` |
| Session splice | `awc-011-session-id-mismatch` | `INVALID_INPUT` |
| Empty export, complete claim | `awc-012-empty-actions-complete-claim` | `COMPLETENESS_OVERCLAIM` |
| Non-injective witness ledger | `awc-013-duplicate-action-id` | `INVALID_INPUT` (AWC preflight) |
| Cherry-picked middle hop only | `awc-015-middle-hop-only-export` | `COMPLETENESS_OVERCLAIM` |

Out of scope for v0.1: prompt injection, tool sandbox escape, live MCP fuzzing.
