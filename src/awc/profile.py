from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PROFILE_ID = "awc-v0.1"


@dataclass(frozen=True)
class ConformanceCase:
    case_id: str
    directory: Path
    reference_path: Path
    evidence_path: Path
    expected_path: Path


@dataclass(frozen=True)
class Profile:
    profile_id: str
    root: Path
    spec_path: Path
    manifest_path: Path
    cases: tuple[ConformanceCase, ...]


def _profile_dir(profile_id: str, repo_root: Path | None = None) -> Path:
    root = repo_root or REPO_ROOT
    return root / "fixtures" / "profiles" / profile_id


def load_profile(profile_id: str = DEFAULT_PROFILE_ID, repo_root: Path | None = None) -> Profile:
    root = _profile_dir(profile_id, repo_root)
    spec_files = {"awc-v0.1": "awc-profile-v0.1.json"}
    spec_name = spec_files.get(profile_id)
    if not spec_name:
        raise ValueError(f"unknown profile_id: {profile_id!r}")
    spec_path = (repo_root or REPO_ROOT) / "spec" / spec_name
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"profile manifest not found: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    cases: list[ConformanceCase] = []
    for entry in manifest.get("cases", []):
        case_id = entry["id"]
        case_dir = root / "cases" / case_id
        cases.append(
            ConformanceCase(
                case_id=case_id,
                directory=case_dir,
                reference_path=case_dir / "reference.json",
                evidence_path=case_dir / "evidence.json",
                expected_path=case_dir / "expected.json",
            )
        )

    if not cases:
        raise ValueError(f"profile {profile_id!r} declares no cases")

    return Profile(
        profile_id=profile_id,
        root=root,
        spec_path=spec_path,
        manifest_path=manifest_path,
        cases=tuple(cases),
    )
