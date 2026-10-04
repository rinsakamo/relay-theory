#!/usr/bin/env python3
"""Actually acquired publisher-original PDF, independent bounded source-anchor tests.
No OCR, no equation-glyph semantic automation, no historical likelihood refit.
"""
import hashlib
import pathlib
import re
import subprocess
import sys
import unittest

ORIGINAL="bc84d4827df202cf5051cf10aa64cc09673b718af2acd31441a3712bcd376df9"
EXPECTED_SIZE=377245
EXPECTED_PAGES=14

ANCHORS=[
  (1, "original publication and article title", r"Actions,\s+Action Sequences and Habits"),
  (2, "original hierarchical-vs-flat Fig 1", r"Figure\s+1\.\s+An example illustrating"),
  (3, "original task 70-30 and reset Fig 2", r"Figure\s+2\.\s+Task description"),
  (4, "original Fig 3 source data", r"Figure\s+3\.\s+"),
  (5, "first-stage models both qualitatively similar, Fig 4", r"Figure\s+4\.\s+Simulation of the first-stage choices"),
  (6, "discriminating stage-2 Fig 5 source data and both model simulations", r"Figure\s+5\.\s+Second-stage choices"),
  (7, "reaction-time original Fig 7 and conditional caveat", r"Figure\s+7\.\s+Reaction times"),
  (8, "bounded conditional inference tree Fig 8", r"Figure\s+8\.\s+Effect of reward"),
  (9, "original source-defined eight-each Table 1 and Table 2", r"Table\s+1\.\s+Model comparison"),
  (10, "both models miss two patterns; original confound and inhibition", r"Deviations from prediction"),
  (11, "real participant task and number of trials", r"Fifteen English speaking subjects"),
  (12, "original MB/MF Q and eq7 conditional eligibility", r"In the trials in which the best action"),
  (13, "original hierarchy original Eq10/11/12/13 discussion", r"Hierarchical model-based,\s+sequence-based RL"),
]
class PDFSourceAnchors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "/tmp/pf04_publisher/publisher_original.pdf")
        actual=cls.path.read_bytes()
        assert actual.startswith(b"%PDF"), "not actual publisher PDF"
        assert b"%%EOF" in actual[-1024:], "publisher original PDF truncated"
        assert len(actual)==EXPECTED_SIZE, "actual publisher original size mismatch"
        assert hashlib.sha256(actual).hexdigest()==ORIGINAL, "FATAL: nonfrozen publisher PDF edition"
        i=subprocess.check_output(["pdfinfo",str(cls.path)],text=True)
        pages=int(re.search(r"^Pages:\s*(\d+)",i,re.M).group(1))
        assert pages==EXPECTED_PAGES,pages
        print("PF04_PUBLISHER_ACTUAL_BYTES_SHA256",ORIGINAL,"size",len(actual),"pages",pages,flush=True)
    def test_actual_pdf_source_anchors(self):
        for p,title,expression in ANCHORS:
            with self.subTest(source_page=p,claim=title):
                txt=subprocess.check_output(["pdftotext","-f",str(p),"-l",str(p),"-layout",str(self.path),"-"],text=True)
                if not re.search(expression,txt,flags=re.I|re.S):
                    self.fail(f"Missing original source primary anchor page {p}: {title}")
                print("PF04_REAL_PDF_ANCHOR_PASS",p,title,flush=True)
    def test_page9_two_source_defined_model_tables(self):
        txt=subprocess.check_output(["pdftotext","-f","9","-l","9","-layout",str(self.path),"-"],text=True)
        self.assertRegex(txt, r"Table\s+1")
        self.assertRegex(txt, r"Table\s+2")
        self.assertRegex(txt, r"0[.]993")
        self.assertRegex(txt, r"0[.]006")
    def test_page13_method_eq_10_to_eq_15_section_present(self):
        txt=subprocess.check_output(["pdftotext","-f","13","-l","13","-layout",str(self.path),"-"],text=True)
        for phrase in ("A1A1","A1A2","model selection","sequence"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(),txt.casefold())
        # Exact Greek glyph for suspect original equation 10 and 13 was manually
        # inspected in publisher raster separately. This test is NOT a glyph proof.
if __name__=="__main__":
    unittest.main(argv=[sys.argv[0]],verbosity=2)
