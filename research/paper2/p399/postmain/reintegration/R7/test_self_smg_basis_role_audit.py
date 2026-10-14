"""Fail-closed integrity checks for R7's bounded post-MAIN source audit.

This is NOT a replay of external sources or a MAIN40 scientific adjudication.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest


MANIFEST = Path(__file__).with_name("SELF_SMG_BASIS_ROLE_AUDIT_v1.json")
BASIS = ("S", "Pi", "K", "O", "T", "C", "Q", "P")
EXPECTED_SOURCES = {
    "S545": "291417539497f42269af9a15512cea320f375310",
    "M0": "4bdc9daf0444e55908cff321111bae9a2927942c",
    "M2": "1e52eccf430fd16f4230e3387e3d2ff31891820d",
    "G4": "2a3e85826d1aeb9241006578da0dcf5932107bd3",
    "V2": "5131bee88cbed6d116d265398f43fd4e7b69c21e",
}
EXPECTED_OBSERVATIONS = {
    "S_B0_SENSING", "S_DEV_RUNTIME", "M0_PHYSICS", "M2_SELECTION",
    "G4_VARIATION", "G3_RECEIPTS", "V_KNOCKDOWN",
}
EXPECTED_GAPS = {
    "WORLD_METABOLIC_CLOCK_JOIN", "M2_G3_AUTHENTIC_BIRTH",
    "S_G_PRODUCTION_ADMISSION", "OWNER_LOCAL_AND_CENTRALIZATION",
    "PHYSICAL_AND_SCIENTIFIC_GATES",
}


def validate(data: dict) -> None:
    if data.get("schema") != "relaytheory.p399.postmain.r7.smg_basis_role_audit.v1":
        raise ValueError("unrecognized R7 audit schema")
    if data.get("class") != "POSTMAIN_ENGINEERING_SOURCE_REVIEW_ONLY":
        raise ValueError("incorrect evidential class")
    if data.get("terminal_classification") != (
        "NO_NEW_TOP_LEVEL_ROLE_WITNESS_IN_PINNED_SMG_SCOPE_WITH_UNQUALIFIED_CROSS_LANE_BRIDGES"
    ):
        raise ValueError("unauthorized scientific promotion or role-gap claim")
    authority = data.get("authority", {})
    if authority.get("working_basis") != list(BASIS):
        raise ValueError("frozen B_P2 modified")
    if authority.get("grammar_v0_distinct_from_basis") is not True:
        raise ValueError("Grammar v0 and B_P2 collapsed")
    r6 = authority.get("r6", {})
    if r6.get("head") != "9a134b25380c4302830c8d567e5ff52870a7b9ef":
        raise ValueError("R6 authority drift")
    if r6.get("status") != "FROZEN_UNMODIFIED":
        raise ValueError("R6 changed")
    main = authority.get("main40", {})
    frozen = {
        "count": 40, "component": 24, "integrated": 16,
        "A0": 40, "A1": 0, "A2": 0,
        "status": "FROZEN_UNMODIFIED", "scientific_role_gap_re_adjudicated": False,
    }
    if any(main.get(key) != value for key, value in frozen.items()):
        raise ValueError("MAIN40 rewritten or reinterpreted")

    sources = data.get("pinned_sources")
    if not isinstance(sources, list) or len(sources) != len(EXPECTED_SOURCES):
        raise ValueError("missing pinned source inventory")
    by_id = {x.get("id"): x for x in sources}
    if set(by_id) != set(EXPECTED_SOURCES):
        raise ValueError("source IDs changed")
    if len(by_id) != len(sources):
        raise ValueError("duplicate source IDs")
    for source_id, sha in EXPECTED_SOURCES.items():
        source = by_id[source_id]
        if source.get("repo") != "rinsakamo/relay-self" or source.get("head") != sha:
            raise ValueError("unpinned or substituted source")
        if not isinstance(source.get("pr"), int) or source.get("pr") <= 0:
            raise ValueError("missing PR locator")
        if not isinstance(source.get("paths"), list):
            raise ValueError("missing code scope")

    observations = data.get("observations")
    if not isinstance(observations, list):
        raise ValueError("missing observations")
    ids = [x.get("id") for x in observations]
    if set(ids) != EXPECTED_OBSERVATIONS or len(ids) != len(EXPECTED_OBSERVATIONS):
        raise ValueError("missing/duplicate observation or invented result")
    for obs in observations:
        roles = obs.get("roles")
        if not isinstance(roles, list) or not roles or len(roles) != len(set(roles)):
            raise ValueError("role inventory malformed")
        if not set(roles) <= set(BASIS):
            raise ValueError("unadjudicated top-level basis role")
        src = obs.get("sources")
        if not isinstance(src, list) or not src or not set(src) <= set(by_id):
            raise ValueError("unknown source reference")
        if obs.get("result") not in {
            "BOUNDED_COMPATIBLE", "BOUNDED_COMPATIBLE_WITH_UNQUALIFIED_SOURCE", "DESIGN_ONLY"
        }:
            raise ValueError("unqualified compatibility label")
        if not obs.get("finding") or not obs.get("limit"):
            raise ValueError("scope or limitation dropped")

    gaps = data.get("open_boundaries")
    if not isinstance(gaps, list):
        raise ValueError("missing open bridge gates")
    gap_ids = [x.get("id") for x in gaps]
    if set(gap_ids) != EXPECTED_GAPS or len(gap_ids) != len(EXPECTED_GAPS):
        raise ValueError("cross-lane gate silently erased")
    for gap in gaps:
        if gap.get("status") not in {
            "UNQUALIFIED", "PARTIALLY_AUDITED", "NOT_ESTABLISHED"
        } or not gap.get("risk") or not gap.get("required"):
            raise ValueError("gap promoted or weakly described")

    flags = data.get("explicit_nonclaims", {})
    if flags.get("no_new_top_level_role_witness_found_in_reviewed_sources") is not True:
        raise ValueError("bounded conclusion missing")
    for key in (
        "unique_or_complete_basis_proved", "all_live_paths_audited",
        "main40_changed", "paper2_role_gap_re_adjudicated",
        "central_coordinator_universally_impossible",
        "full_smg_integration_qualified", "field_and_science_success",
    ):
        if flags.get(key) is not False:
            raise ValueError(f"scientific or universal promotion forbidden: {key}")


class AuditIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_frozen_audit_valid(self) -> None:
        validate(self.data)

    def test_basis_corruption_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["authority"]["working_basis"].append("NEW")
        with self.assertRaises(ValueError):
            validate(sample)

    def test_main40_rewrite_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["authority"]["main40"]["A1"] = 1
        with self.assertRaises(ValueError):
            validate(sample)

    def test_source_drift_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["pinned_sources"][0]["head"] = "current"
        with self.assertRaises(ValueError):
            validate(sample)

    def test_extra_role_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["observations"][0]["roles"].append("GENESIS_NEW_PRIMITIVE")
        with self.assertRaises(ValueError):
            validate(sample)

    def test_missing_bridge_gate_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["open_boundaries"].pop()
        with self.assertRaises(ValueError):
            validate(sample)

    def test_science_promotion_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["explicit_nonclaims"]["field_and_science_success"] = True
        with self.assertRaises(ValueError):
            validate(sample)

    def test_role_gap_promotion_rejected(self) -> None:
        sample = copy.deepcopy(self.data)
        sample["authority"]["main40"]["scientific_role_gap_re_adjudicated"] = True
        with self.assertRaises(ValueError):
            validate(sample)


if __name__ == "__main__":
    unittest.main(verbosity=2)
