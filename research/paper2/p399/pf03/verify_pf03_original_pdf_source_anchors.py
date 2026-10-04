#!/usr/bin/env python3
"""PF03 post-E independent, bounded *real published PDF* source-anchor audit.
Only publisher-PDF claims, not secondary author code, original full numerical
replication or the separately archived exact #401 v2.3.1 software validator.
A page number in this test is the zero-based index of the 30-page printed PDF.
"""
import hashlib
import re
import sys
import unittest
from pathlib import Path

from pypdf import PdfReader

FROZEN_PUBLISHER_SHA="62d744125034ce834692cdb210065d34e2bbd0f58c9eb3387ed2d75dfb7f77ae"
FROZEN_BYTES=3333319
def norm(s):
    return re.sub(r"\s+"," ",s.replace("\u00ad","").replace("\x00","")).lower()
def anchor(s,*terms):
    return all(norm(term) in s for term in terms)
class PF03PublishedSourceAnchors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=Path(sys.argv[1])
        dat=cls.path.read_bytes()
        if not dat.startswith(b"%PDF"):
            raise AssertionError("not actual original PDF")
        if len(dat)!=FROZEN_BYTES or hashlib.sha256(dat).hexdigest()!=FROZEN_PUBLISHER_SHA:
            raise AssertionError("publisher source does not match frozen 2024 original before A")
        reader=PdfReader(cls.path)
        if len(reader.pages)!=30:
            raise AssertionError("wrong 30-page original")
        cls.p=[norm(page.extract_text() or "") for page in reader.pages]
        if any(len(p)<100 for p in cls.p):
            raise AssertionError("unreadable source page")
    def test_01_original_pdf_identity_and_page_coverage(self):
        self.assertEqual(len(self.p),30)
        self.assertTrue(anchor(self.p[0],"dynamic predictive coding","jiang","rao","2024","1011801"))
    def test_02_lower_and_higher_model_top_down_not_neural_feedback_to_external_world(self):
        self.assertTrue(anchor(self.p[2],"modulation","transition","hypernetwork"))
        self.assertTrue(anchor(self.p[3],"prediction error","higher","lower"))
    def test_03_measured_time_scales_original_report_only(self):
        self.assertTrue(anchor(self.p[6],"5.49","2.18","autocorrelation"))
    def test_04_two_level_bounce_limit_and_content_direction_decoding(self):
        self.assertTrue(anchor(self.p[6],"bounced","higher-level","prediction errors"))
        self.assertTrue(anchor(self.p[7],"76.1%","20.9%"))
    def test_05_flash_lag_initial_trajectory_adverse_null(self):
        self.assertTrue(anchor(self.p[9],"initial trajectories","no effects","flash-lag"))
    def test_06_early_late_correction_not_actual_human_neural_delay(self):
        self.assertTrue(anchor(self.p[10],"10%","90%","350 ms","620 ms"))
    def test_07_optional_memory_component_training_scope_and_negative_cues(self):
        self.assertTrue(anchor(self.p[11],"associative memory","sequence"))
        self.assertTrue(anchor(self.p[12],"only the weights","starting frame","middle frame","end frame","weak recall","did not trigger recall"))
    def test_08_third_level_original_figure_gated_subsequence_and_representation(self):
        self.assertTrue(anchor(self.p[13],"first-level prediction error","threshold","bouncing","direction"))
        self.assertTrue(anchor(self.p[14],"third-level","straight","clockwise","stable"))
    def test_09_original_discussion_excludes_unimplemented_online_gate_and_action_world_loop(self):
        self.assertTrue(anchor(self.p[17],"post-hoc","threshold","future","action-conditioned"))
    def test_10_original_2_level_generative_initial_factor_and_first_step_exception(self):
        self.assertTrue(anchor(self.p[18],"hierarchical generative model","parameter","temporal"))
        self.assertTrue(anchor(self.p[19],"begin","first step","reduced","temporal prediction","summed across time"))
    def test_11_original_memory_conditional_only_as_optional_augmented_network(self):
        self.assertTrue(anchor(self.p[22],"associative memory","memory layer","fixed"))
        self.assertTrue(anchor(self.p[23],"partial input","binary mask","visual cue"))
    def test_12_original_3level_event_gate_and_distinct_upper_loss_from_primary(self):
        self.assertTrue(anchor(self.p[23],"pretraining","second-level","first-level prediction error","threshold","training"))
        self.assertTrue(anchor(self.p[23],"third-level","transition matrices","same loss"))
    def test_13_no_secondary_implementation_exact_scalar_presented_as_primary(self):
        # Author's code determines *its* squared prior-versus-posterior temporal
        # latent score, but the original publication names first-level
        # prediction error without unambiguously defining its exact numeric
        # source-expression for gating.
        s=self.p[23]
        self.assertTrue(anchor(s,"first-level prediction error","larger than a threshold"))
        self.assertTrue(anchor(s,"fig c in s1 text"))
        self.assertFalse(anchor(s,"orig_r2","r2_loss"))
    def test_14_scope_specific_figure_vs_math_independent_render_review(self):
        # Dedicated human/vision review separately inspected rendered Eq37,
        # Fig6, Eqs3-9 and distinct memory mask (Eq36). These text anchors
        # are not proof that pypdf preserved each visual math glyph.
        self.assertTrue(anchor(self.p[23],"second-level","third-level","binary mask"))
        self.assertTrue(anchor(self.p[18],"hierarchical generative model"))
    def test_15_tampered_exact_primary_fails_closed(self):
        data=self.path.read_bytes()
        self.assertNotEqual(hashlib.sha256(data+b" ").hexdigest(),FROZEN_PUBLISHER_SHA)
if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: python verify_pf03_original_pdf_source_anchors.py ORIGINAL_PDF_PATH")
    unittest.main(argv=[sys.argv[0]],verbosity=2)
