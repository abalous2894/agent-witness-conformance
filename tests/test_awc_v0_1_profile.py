from __future__ import annotations

from pathlib import Path

from awc.profile import load_profile
from awc.runner import run_profile

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_manifest_lists_fifteen_cases() -> None:
    profile = load_profile("awc-v0.1", repo_root=REPO_ROOT)
    assert len(profile.cases) == 15


def test_run_profile_awc_v0_1_all_pass() -> None:
    result = run_profile("awc-v0.1", repo_root=REPO_ROOT)
    assert result.failed == 0, [
        (c.case_id, c.errors, c.actual_verdict) for c in result.cases if not c.passed
    ]
    assert result.passed == 15
