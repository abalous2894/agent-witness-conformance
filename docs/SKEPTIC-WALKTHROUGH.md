# Skeptic walkthrough

Goal: verify the author understood witness grading, not that marketing copy matches reality.

## Step 1 — Install reference grader

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e /path/to/witnessdiff
pip install -e .
```

## Step 2 — Run full profile

```bash
awc run-profile awc-v0.1
```

Expect `passed=15 failed=0`.

## Step 3 — Break one fixture on purpose

Edit `fixtures/profiles/awc-v0.1/cases/awc-002-silent-omission/expected.json` and change `"verdict"` to `COMPLETE`. Re-run. The profile **must fail**.

Revert the edit.

## Step 4 — Read one AWC-only rule

Open [src/awc/preflight.py](../src/awc/preflight.py) and [awc-013-duplicate-action-id](../fixtures/profiles/awc-v0.1/cases/awc-013-duplicate-action-id/CASE.md).

Run:

```bash
awc verify -r fixtures/profiles/awc-v0.1/cases/awc-013-duplicate-action-id/reference.json \
           -e fixtures/profiles/awc-v0.1/cases/awc-013-duplicate-action-id/evidence.json
```

WitnessDiff alone would **not** emit `INVALID_INPUT` for duplicate anchors; AWC preflight does. That split is intentional: profile rules vs reference comparator.

## Step 5 — Read claim boundary

[CLAIM-BOUNDARY.md](../CLAIM-BOUNDARY.md) — confirm the project does not over-claim production truth.
