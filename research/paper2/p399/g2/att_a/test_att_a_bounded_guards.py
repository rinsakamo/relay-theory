#!/usr/bin/env python3
import copy
import json
import pathlib
import tempfile
import unittest
from att_a_independent_source_receipt import HANDOFF, FILES, validate_ledger, run

class AttASourceGuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=json.loads(HANDOFF.read_text(encoding="utf8"))

    def assert_rejected(self,mutator):
        record=copy.deepcopy(self.baseline)
        mutator(record)
        with self.assertRaises(AssertionError):
            validate_ledger(record)

    def test_01_real_ledger_guard(self):
        self.assertTrue(validate_ledger(self.baseline))

    def test_02_false_original_sha_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["source_bundle"]["single_primary"].update(prior_raw_sha256="0"*64))

    def test_03_false_s3_sha_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["source_bundle"]["mandatory_same_article_s3"].update(prior_raw_sha256="0"*64))

    def test_04_missing_model_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["published_models"].pop())

    def test_05_missing_negative_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["negative_conditions_upstream_v8_immutable"].pop())

    def test_06_false_model_ranking_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["published_error"]["M3b"].update(mean=0.2))

    def test_07_false_m3a_se_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"]["published_error"]["M3a"].update(se=0.01))

    def test_08_false_main_go_rejected(self):
        self.assert_rejected(lambda x:x["bounded_decision"].update(main_authorized=True))

    def test_09_false_backup_activation_rejected(self):
        self.assert_rejected(lambda x:x["bounded_decision"].update(backups_activated=1))

    def test_10_false_s3_visual_claim_rejected(self):
        self.assert_rejected(lambda x:x["ATT_B1"].update(full_S3_math_eq_S1_to_S19_visual="PASS"))

    def test_11_false_ATT03_official_source_claim_rejected(self):
        self.assert_rejected(lambda x:x["ATT_03"].update(admission="QUALIFIED"))

    def test_12_false_start_head_rejected(self):
        self.assert_rejected(lambda x:x.update(baseline_g2_head="0"*40))

    def test_13_offline_runtime_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence=run(tmp,offline=True)
            self.assertEqual(evidence["ledger_static_guard"],"PASS")
            self.assertEqual(evidence["mode"],"OFFLINE_GUARD_ONLY")
            self.assertEqual(evidence["records"],[])
            self.assertTrue((pathlib.Path(tmp)/"ATT_A_ACTUAL_RUNTIME_RECEIPT.json").is_file())

if __name__=="__main__": unittest.main(verbosity=2)
