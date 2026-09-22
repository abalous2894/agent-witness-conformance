from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from awc.grader import assert_matches_expected, grade_paths
from awc.profile import Profile, load_profile


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    errors: tuple[str, ...]
    actual_verdict: str | None


@dataclass(frozen=True)
class ProfileRunResult:
    profile_id: str
    passed: int
    failed: int
    cases: tuple[CaseResult, ...]


def run_profile(profile_id: str = "awc-v0.1", repo_root: Path | None = None) -> ProfileRunResult:
    profile = load_profile(profile_id, repo_root=repo_root)
    return _run_loaded_profile(profile)


def _run_loaded_profile(profile: Profile) -> ProfileRunResult:
    results: list[CaseResult] = []
    passed = 0
    failed = 0

    for case in profile.cases:
        for path, label in (
            (case.reference_path, "reference.json"),
            (case.evidence_path, "evidence.json"),
            (case.expected_path, "expected.json"),
        ):
            if not path.is_file():
                failed += 1
                results.append(
                    CaseResult(
                        case_id=case.case_id,
                        passed=False,
                        errors=(f"missing {label}: {path}",),
                        actual_verdict=None,
                    )
                )
                break
        else:
            report = grade_paths(case.reference_path, case.evidence_path)
            expected = json.loads(case.expected_path.read_text(encoding="utf-8"))
            errors = assert_matches_expected(report, expected)
            ok = not errors
            if ok:
                passed += 1
            else:
                failed += 1
            results.append(
                CaseResult(
                    case_id=case.case_id,
                    passed=ok,
                    errors=tuple(errors),
                    actual_verdict=report.verdict.value,
                )
            )

    return ProfileRunResult(
        profile_id=profile.profile_id,
        passed=passed,
        failed=failed,
        cases=tuple(results),
    )
