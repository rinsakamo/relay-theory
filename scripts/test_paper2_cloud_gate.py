"""Offline, source-free negative tests for the cloud provenance gate."""
import copy
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paper2_cloud_gate as gate

COMMITS = ["a" * 40, "b" * 40, "c" * 40, "d" * 40, "e" * 40, "f" * 40]
STAGE_BLOBS = {}


def pin(phase, commit):
    path = f"research/paper2/cloud60/records/fixture-{phase.lower()}.json"
    data = ('{"phase":"' + phase + '"}').encode()
    STAGE_BLOBS[(commit, path)] = data
    return dict(phase=phase, commit=commit, path=path,
                sha256=hashlib.sha256(data).hexdigest())


def fake_read(commit, path):
    return STAGE_BLOBS[(commit, path)]


def fake_ancestor(earlier, later):
    return COMMITS.index(earlier) < COMMITS.index(later)


def p399():
    phases = ("SOURCE", "A", "B", "C")
    return {
        "schema": "relay-theory.paper2.cloud-receipt.v1",
        "track": "P399_NEW_PILOT", "run_id": "new-pilot-fixture-1",
        "source_id": "F01", "historical_case": False,
        "source": {
            "canonical_work": "doi:fixture", "url": "https://example.org/article",
            "kind": "PUBLISHER_FULL_HTML", "publisher_designated_complete": True,
            "standalone_supplements": "OUT_OF_SCOPE", "edition_status": "VERIFIED",
            "lineage_status": "VERIFIED_DISTINCT", "family_id": "fixture-family",
            "scope_metadata_sha256": "1" * 64,
        },
        "stages": [pin(name, COMMITS[i]) for i, name in enumerate(phases)],
        "author_exception_review": "NONE_NEEDED",
    }


class CloudGateTest(unittest.TestCase):
    def setUp(self):
        STAGE_BLOBS.clear()

    def check(self, r):
        return gate.validate_receipt(r, fake_read, fake_ancestor)

    def test_new_pilot_provenance_good_is_not_scientific_approval(self):
        self.assertEqual(self.check(p399())[:2],
                         ("P399_NEW_PILOT", "new-pilot-fixture-1"))

    def test_historical_pilot_cannot_rebadge_prospective(self):
        r = p399()
        r["historical_case"] = True
        with self.assertRaises(gate.GateError):
            self.check(r)

    def test_p399_cannot_admit_copy_or_external_supplements(self):
        r = p399()
        r["source"]["kind"] = "VERIFIED_MODEL_EQUIVALENT_COPY"
        with self.assertRaises(gate.GateError):
            self.check(r)
        r = p399()
        r["source"]["standalone_supplements"] = "REQUIRED"
        with self.assertRaises(gate.GateError):
            self.check(r)

    def test_hash_tamper_rejected(self):
        r = p399()
        r["stages"][2]["sha256"] = "0" * 64
        with self.assertRaises(gate.GateError):
            self.check(r)

    def test_phase_gap_and_same_commit_rejected(self):
        r = p399()
        r["stages"][2]["phase"] = "C"
        with self.assertRaises(gate.GateError):
            self.check(r)
        r = p399()
        r["stages"][1]["commit"] = r["stages"][0]["commit"]
        r["stages"][1]["path"] = r["stages"][0]["path"]
        r["stages"][1]["sha256"] = r["stages"][0]["sha256"]
        with self.assertRaises(gate.GateError):
            self.check(r)

    def test_unqualified_source_may_stage_but_not_run(self):
        r = p399()
        r["source"]["edition_status"] = "PENDING"
        r["stages"] = r["stages"][:1]
        self.check(r)
        r["stages"] = p399()["stages"][:2]
        with self.assertRaises(gate.GateError):
            self.check(r)

    def test_p398_verified_copy_accepted_not_forced_to_html(self):
        r = p399()
        r["track"] = "P398_PRETEST"
        r.pop("historical_case")
        r.pop("author_exception_review")
        r["source"]["kind"] = "VERIFIED_MODEL_EQUIVALENT_COPY"
        r["source"]["copy_sha256"] = "2" * 64
        r["source"]["equivalence_evidence"] = "source-checked version/equation audit"
        r["stages"] = r["stages"][:1]
        self.assertEqual(self.check(r)[0], "P398_PRETEST")

    def test_p398_main_requires_frozen_roster_and_pilot_protocol(self):
        r = p399()
        r["track"] = "P398_MAIN"
        r.pop("historical_case")
        r.pop("author_exception_review")
        r["stages"] = [pin(phase, COMMITS[i + 2])
                       for i, phase in enumerate(("SOURCE", "REFERENCE", "MASKED", "RECONSTRUCTION"))]
        r["masking_and_leakage_record"] = "separate masked evidence ledger"
        with self.assertRaises(gate.GateError):
            self.check(r)
        r["locks"] = {
            "main_manifest": pin("MAIN_ROSTER", COMMITS[0]),
            "pilot_protocol": pin("PROTOCOL", COMMITS[1]),
        }
        r["pilot_qualification"] = "HUMAN_REVIEWED_AND_FROZEN"
        self.assertEqual(self.check(r)[0], "P398_MAIN")

    def test_main_and_pretest_identical_family_is_not_allowed(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "a.json").write_text('{"key":"a"}', encoding="utf8")
            Path(directory, "b.json").write_text('{"key":"b"}', encoding="utf8")
            with patch.object(gate, "validate_receipt",
                              side_effect=[("P398_PRETEST", "run-a", "work-a", "same-family"),
                                           ("P398_MAIN", "run-b", "work-b", "same-family")]):
                with self.assertRaises(gate.GateError):
                    gate.validate_directory(directory)


if __name__ == "__main__":
    unittest.main()
