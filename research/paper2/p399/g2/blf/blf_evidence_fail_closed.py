#!/usr/bin/env python3
"""G2-B source-metadata regression only. This does not validate science/PDF pixels."""
import copy
import hashlib
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "BLF_BOUNDED_ORIGINAL_AND_FAMILY_DECISION_v1.json"
START = "69748673c80f421605f1c63607472903ac2ed68c"
G1 = "38c5eb24c61b9e57371084a65fcbcb9fb9c62a4b"
B1_SHA = "869c8b1a535fcb4a922d677bc0c26ca8959930a7f62208c4bf74701899aa8870"
PMC_SHA = "68369c258b53098c934f6f3c8c2c29d1c16c8236df50e61040fd55b3b6b76c52"
B2_SHA = "7b6e4192bfe1b60d794d197e14822997b77d22e437db89850fc4cddcb79482db"


def qualified(d):
    """Fail closed on unsupported promotions, even with plausible valid DOIs."""
    a, s, x, f, b, g, scope = (
        d["authority"], d["blf01"], d["blfb1"], d["family_comparison"],
        d["blfb2"], d["global"], d["scope"]
    )
    assert a["immutable_start_sha"] == START and a["observed_g1_sha"] == G1
    assert a["g2_backup_registration_blob"] == "f86d4aa2e4b4a6f46d8c46dab90cdd12447479ff"
    assert a["g2_v5_roster_blob"] == "b97b67a34ad9c2858745dfa6aa60444520eaab13"
    assert d["schema"].endswith("v1") and d["date_jst"] == "2026-10-04"
    assert s["publisher_primary_pdf_recovered"] is False
    assert s["publisher_complete_primary_html_recovered"] is False
    assert s["original_edition_scientific_admitted"] is False
    assert s["archive"]["original_legacy_raw_sha256"] == PMC_SHA
    assert s["archive"]["publisher_original_byte_identity_proven"] is False
    assert s["archive"]["publisher_original_edition_equivalence_proven"] is False
    assert s["archive"]["archive_not_substituted_for_publisher"] is True
    assert s["decision"] == "HOLD_PUBLISHER_ORIGINAL_NOT_VERIFIED"
    assert x["predeclared_rank"] == 1
    assert x["publisher_pdf"]["prior_physical_retrieval_verified"] is True
    assert x["publisher_pdf"]["raw_sha256"] == B1_SHA
    assert x["publisher_pdf"]["pages"] == 19
    assert x["publisher_pdf"]["current_session_all_19_pdf_pages_pixel_audited"] is False
    assert x["publisher_correction"]["doi"] == "10.1371/journal.pcbi.1003952"
    assert x["publisher_correction"]["notice_reports_model_formula_change"] is False
    assert x["publisher_correction"]["no_other_corrections_exhaustively_proven"] is False
    assert x["model_inventory"]["factorial_model_count_publisher_stated"] == 12
    assert len(x["model_inventory"]["perceptual_classes"]) == 3
    assert len(x["model_inventory"]["response_factorial_classes"]) == 4
    assert x["scientific_native_review"]["math_pdf_pixels_all_verified"] is False
    assert x["scientific_native_review"]["original_full_source_semantic_scientific_qualification"] is False
    assert x["decision"] == "PHYSICAL_ORIGINAL_CONFIRMED_SCIENTIFIC_SCOPE_HOLD"
    p = f["blfb1_to_blf02"]
    assert p["shared_ancestor"] == "Mathys et al. 2011 cited in both originals"
    assert p["direct_blfb1_to_blf02_derivation_proven"] is False
    assert p["full_original_equation_pixel_pairwise_and_whole_family_review_complete"] is False
    assert "UNDERDETERMINED" in p["decision"]
    assert f["with_g1"]["g1_observed_bounded_qualified"] == 9
    assert f["with_g1"]["g1_final_roster_frozen"] is False
    assert f["with_g1"]["g1_p07"]["blfb1_original_direct_reference"] is True
    assert f["global_final_family_independence"] is False
    assert b["predeclared_rank"] == 2 and b["conditional_trigger_met"] is False
    assert b["scientific_review_not_started_in_this_lane"] is True
    assert b["prior_official_pdf_source_receipt"]["raw_sha256"] == B2_SHA
    assert set(b["also_reserved"]) == {"PRD-B2", "LRN-B2"}
    assert b["multi_slot_activation_permitted"] is False and b["decision"] == "DORMANT_NO_CONDITIONAL_ADMISSION"
    assert g["existing_main40_working_dois"] == 40
    assert g["allocation_component"] == 24 and g["allocation_integration"] == 16
    assert g["g2_final_original_math_figure_variant_admissions"] == 0
    assert g["g2_final_central_family_admissions"] == 0
    assert g["backup_activations"] == 0 and g["author_GO"] is False
    assert g["final_manifest_not_modified"] is True
    assert all(scope[k] is False for k in (
        "MAIN_decomposition", "MAIN_Grammar_mapping", "MAIN_H_classification",
        "MAIN_scientific_execution", "preliminary_MAIN_outcomes_read",
        "shared_MAIN40_edited", "backup_activated", "MAIN_authorized",
        "original_398_changed"))
    return True


class BoundedScienceGuards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(DATA.read_bytes())

    def test_00_real_checked_out_record(self):
        self.assertTrue(qualified(self.base))

    def _must_reject(self, change):
        test = copy.deepcopy(self.base)
        change(test)
        with self.assertRaises(AssertionError):
            qualified(test)

    def test_01_fake_pmc_publisher_equivalence(self):
        self._must_reject(lambda x: x["blf01"]["archive"].update(
            publisher_original_edition_equivalence_proven=True))

    def test_02_fake_unobtained_original_success(self):
        self._must_reject(lambda x: x["blf01"].update(publisher_primary_pdf_recovered=True))

    def test_03_forged_publisher_source_checksum(self):
        self._must_reject(lambda x: x["blfb1"]["publisher_pdf"].update(raw_sha256="0" * 64))

    def test_04_fake_full_pdf_pixel_certification(self):
        self._must_reject(lambda x: x["blfb1"]["scientific_native_review"].update(
            math_pdf_pixels_all_verified=True))

    def test_05_fake_global_model_independence(self):
        self._must_reject(lambda x: x["family_comparison"].update(global_final_family_independence=True))

    def test_06_forged_final_g1_roster(self):
        self._must_reject(lambda x: x["family_comparison"]["with_g1"].update(g1_final_roster_frozen=True))

    def test_07_illicit_rank_two_activation(self):
        self._must_reject(lambda x: x["blfb2"].update(conditional_trigger_met=True))

    def test_08_duplicate_shared_backup(self):
        self._must_reject(lambda x: x["blfb2"].update(multi_slot_activation_permitted=True))

    def test_09_fake_main_authorization(self):
        self._must_reject(lambda x: x["global"].update(author_GO=True))

    def test_10_fake_scientific_admission_count(self):
        self._must_reject(lambda x: x["global"].update(g2_final_central_family_admissions=40))

    def test_11_unauthorized_main_execution(self):
        self._must_reject(lambda x: x["scope"].update(MAIN_scientific_execution=True))

    def test_12_false_model_count(self):
        self._must_reject(lambda x: x["blfb1"]["model_inventory"].update(factorial_model_count_publisher_stated=13))


if __name__ == "__main__":
    print("SOURCE_RECORD_RAW_SHA256", hashlib.sha256(DATA.read_bytes()).hexdigest())
    unittest.main(verbosity=2)
