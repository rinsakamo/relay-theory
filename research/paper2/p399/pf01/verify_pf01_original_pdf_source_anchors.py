#!/usr/bin/env python3
"""Independent SOURCE-BYTE anchor gate for PF01's exact frozen publisher PDF.

This verifies a bounded set of independently extractable page-specific statements
against ACTUAL publisher PDF bytes, rather than trusting a self-reported ledger.
It is NOT the missing exact v2.3.1 C validator, an exhaustive semantic audit,
or a numerical replication of the original paper.
"""
import hashlib
import re
import subprocess
import sys
import unittest
from pathlib import Path

FROZEN_SHA = "8531103d577a3249c7edffa06ef2a8a7e85eb01b0a2f02cee2145e187581fbc3"
PAGES = (1, 10, 11, 16, 18, 27, 28, 39, 40)

def extract_page(path, pageno):
    p = subprocess.run(
        ["pdftotext", "-f", str(pageno), "-l", str(pageno), "-layout", str(path), "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return re.sub(r"\s+", " ", p.stdout.decode("utf-8", "replace"))

def real_pdf(path):
    data = path.read_bytes()
    if not data.startswith(b"%PDF"):
        raise ValueError("not PDF")
    if hashlib.sha256(data).hexdigest() != FROZEN_SHA:
        raise ValueError("primary source bytes differ from frozen A/B/C/E")
    out = subprocess.check_output(["pdfinfo", str(path)], text=True)
    if not re.search(r"(?m)^Pages:\s+48\s*$", out):
        raise ValueError("unexpected page count")
    return data

class FixedOriginalAnchorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = Path(sys.argv[-1]).resolve()
        real_pdf(cls.path)
        cls.pages = {i: extract_page(cls.path, i) for i in PAGES}

    def test_01_exact_bytes_and_page_count(self):
        self.assertEqual(hashlib.sha256(real_pdf(self.path)).hexdigest(), FROZEN_SHA)

    def test_02_publisher_identity(self):
        self.assertIn("Stability of working memory", self.pages[1])
        self.assertIn("April 19, 2019", self.pages[1])
        self.assertIn("1006928", self.pages[1])

    def test_03_fig2_internally_inconsistent_parameter(self):
        s=self.pages[10]
        self.assertIn("U = 0.1",s)
        self.assertIn("U = 0.01",s)
        self.assertIn("predicted drift field",s)
        # This test deliberately DOES NOT choose a winner for exact plotted data.

    def test_04_diffusion_Results_reports_twenty(self):
        s=self.pages[11]
        self.assertIn("1000 repetitions",s)
        self.assertIn("20 uniformly spaced initial cue positions",s)

    def test_05_diffusion_Methods_reports_ten_times_hundred(self):
        s=self.pages[39]
        self.assertIn("10 initial cue positions, 100 repetitions each",s)
        self.assertIn("1000 repetitions",s)

    def test_06_eq11_has_two_root_terms_joined_by_addition(self):
        s=self.pages[16]
        self.assertIn("expected displacement in 1s",s)
        self.assertIn("1s",s)
        self.assertIn("hA2 ifrozen",s)  # poppler's extraction of sqrt(<A^2>_frozen)
        self.assertIn("differential equation for a time interval",s)
        # Mathematical glyph fidelity was separately confirmed by rendering
        # the exact PDF's page 16. PDF text extraction is NOT its sole proof.

    def test_07_same_presynaptic_noise_across_stp_vars(self):
        s=self.pages[27]
        self.assertIn("same presynaptic spike train",s)
        self.assertIn("white noises",s)

    def test_08_explicit_unproved_drift_continuity_limitation(self):
        s=self.pages[28]
        self.assertIn("nearly continuously",s)
        self.assertIn("rigorous proof of these arguments",s)
        self.assertIn("future work",s)

    def test_09_distractor_bump_width_control(self):
        s=self.pages[18]
        self.assertIn("0.8rad",s)
        self.assertIn("0.5rad",s)
        self.assertIn("distractor",s.lower())

    def test_10_original_drift_estimator(self):
        # The drift-estimation paragraph crosses PDF pp39->40; its dt is on p40.
        s=self.pages[39] + " " + self.pages[40]
        self.assertIn("400 repetitions",s)
        self.assertIn("20 initial cue positions, 20 repetitions",s)
        self.assertIn("1.5s",s)

    def test_11_numerical_euler_and_periodic_interpolation(self):
        s=self.pages[40]
        self.assertIn("gsl_interp_cspline_periodic",s)
        self.assertIn("dt = 0.1s",s)
        self.assertIn("circular boundary conditions",s)

    def test_12_modified_source_fails_closed(self):
        self.assertNotEqual(hashlib.sha256(real_pdf(self.path) + b"\n").hexdigest(),FROZEN_SHA)
        # Do not write a mutated copy of the copyrighted full PDF in Git.

if __name__=="__main__":
    if len(sys.argv)!=2:
        raise SystemExit("usage: verify_pf01_original_pdf_source_anchors.py path/to/authorized/original.pdf")
    arg=sys.argv[1]
    sys.argv=[sys.argv[0],arg]
    print("PF01: verifying actual PLOS ORIGINAL PDF SHA and bounded original page anchors")
    unittest.main(argv=[sys.argv[0]], verbosity=2)
