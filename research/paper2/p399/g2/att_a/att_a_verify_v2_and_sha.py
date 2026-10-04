#!/usr/bin/env python3
"""ATT-A only: immutable source lineage, post-S3-pixel qualification boundary and actual SHA256 inventory."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[4]
BASE="69748673c80f421605f1c63607472903ac2ed68c"
G2="research/paper2/p399/g2/"
V8="MAIN40_G2_V8_ATT_B1_PRE_A_PRIMARY_PLUS_DEFINING_S3_SOURCE_BUNDLE.json"
V8A="MAIN40_G2_V8A_ATT_B1_FIT_NARRATIVE_CONFLICT_APPEND_ONLY.json"
PIXEL=HERE/"ATT_A_ORIGINAL_PDF_PIXEL_SCIENTIFIC_AUDIT_v2.json"
HANDOFF=HERE/"ATT_A_G2_INTEGRATOR_FINAL_BOUNDED_HANDOFF_v2.json"

def git(*args):
    return subprocess.check_output(["git",*args],cwd=REPO)

def baseline_file(file):
    return git("show",BASE+":"+G2+file)

def load():
    return json.loads(PIXEL.read_bytes()),json.loads(HANDOFF.read_bytes())

def validate(pixel, handoff):
    assert handoff["snapshot"]["base_exact_sha"]==BASE
    assert handoff["ATT_03"]["admission"]=="HOLD_NO_PUBLISHED_ORIGINAL"
    att=handoff["ATT_B1"]
    assert att["source_math_visual_bounded"]=="PASS"
    assert att["all_criteria_scientific_admission"]=="HOLD"
    assert att["complete_correction_chronology"].startswith("HOLD")
    assert att["printed_metric"]["relative_prose_vs_fit"].startswith("UNDERDETERMINED")
    assert len(att["adverse_prior_ids_unchanged"])==8
    assert att["adverse_new"].startswith("N_ATT_B1_009")
    assert att["original_modelling"].startswith("YES")
    assert att["scientific_visual_evidence"]["s3_S1_to_S19"].startswith("VISUALLY")
    assert att["physical_evidence"]["cloud_guard_tests"]=="13/13_PASS"
    assert handoff["native_genealogy"]["G1_final20"]=="UNFROZEN"
    assert all(v is False for v in handoff["authorization"].values())
    assert pixel["originals"]["s3"]["all_six_individually_rendered_and_visual_inspected"]
    eq=set()
    for page in pixel["originals"]["s3"]["eq_visual_page_map"]:
        eq.update(page["eq"])
    assert eq=={f"S{i}" for i in range(1,20)}
    assert pixel["originals"]["s3"]["all_four_parameter_tables_visually_identified"]
    assert pixel["fit_published_native_composite"]["assessment"].startswith("UNDERDETERMINED")
    assert pixel["originals"]["main"]["all_20_individually_visual_reviewed"] is False
    assert pixel["backup_activated"] is False and pixel["main_authorized"] is False
    assert att["official_primary"]["sha256"]==pixel["originals"]["main"]["exact_pdf_sha256"]
    assert att["official_mandatory_same_paper_s3"]["sha256"]==pixel["originals"]["s3"]["exact_pdf_sha256"]
    return True

class ActualATTSourceLineage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p,cls.h=load()

    def test_current_science_source_guard(self):
        self.assertTrue(validate(self.p,self.h))

    def test_actual_baseline_commit_is_ancestor(self):
        subprocess.run(["git","merge-base","--is-ancestor",BASE,"HEAD"],cwd=REPO,check=True)

    def test_actual_v8_source_hashes_match_immutable_base(self):
        raw=baseline_file(V8)
        j=json.loads(raw)
        self.assertEqual(j["exact_standby"]["primary"]["published_firstparty_raw_sha256"],self.h["ATT_B1"]["official_primary"]["sha256"])
        self.assertEqual(j["exact_standby"]["mandatory_original_mathematics_companion"]["published_firstparty_raw_sha256"],self.h["ATT_B1"]["official_mandatory_same_paper_s3"]["sha256"])
        self.assertEqual(git("show","HEAD:"+G2+V8),raw)

    def test_actual_v8a_unresolved_history_retained(self):
        raw=baseline_file(V8A)
        j=json.loads(raw)
        self.assertEqual(j["first_observation"]["se"],0.01)
        self.assertTrue(self.h["ATT_B1"]["historical_v8a_single_field_M3a_se_0_01"].startswith("RECORD_INCONSISTENCY"))
        self.assertEqual(git("show","HEAD:"+G2+V8A),raw)

    def test_fake_authorization_rejected(self):
        h=copy.deepcopy(self.h)
        h["authorization"]["MAIN_authorized"]=True
        with self.assertRaises(AssertionError): validate(self.p,h)

    def test_fake_S3_math_rejected(self):
        h=copy.deepcopy(self.h)
        h["ATT_B1"]["scientific_visual_evidence"]["s3_S1_to_S19"]="UNREAD"
        with self.assertRaises(AssertionError): validate(self.p,h)

    def test_fake_equation_omission_rejected(self):
        p=copy.deepcopy(self.p)
        p["originals"]["s3"]["eq_visual_page_map"][2]["eq"].remove("S12")
        with self.assertRaises(AssertionError): validate(p,self.h)

    def test_fake_no_conflict_rejected(self):
        h=copy.deepcopy(self.h)
        h["ATT_B1"]["printed_metric"]["relative_prose_vs_fit"]="RESOLVED"
        with self.assertRaises(AssertionError): validate(self.p,h)

    def test_fake_missing_negative_009_rejected(self):
        h=copy.deepcopy(self.h)
        h["ATT_B1"]["adverse_new"]="NONE"
        with self.assertRaises(AssertionError): validate(self.p,h)

    def test_fake_publication_qualified_rejected(self):
        h=copy.deepcopy(self.h)
        h["ATT_B1"]["all_criteria_scientific_admission"]="PASS"
        with self.assertRaises(AssertionError): validate(self.p,h)

def ledger():
    target=Path("att-a-run")
    target.mkdir(exist_ok=True)
    files=sorted(p for p in HERE.iterdir() if p.is_file() and p.suffix in (".json",".md",".py"))
    entries={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    entries["IMMUTABLE_BASE_"+V8]=hashlib.sha256(baseline_file(V8)).hexdigest()
    entries["IMMUTABLE_BASE_"+V8A]=hashlib.sha256(baseline_file(V8A)).hexdigest()
    out=target/"ATT_A_INDEPENDENT_RAW_SHA256SUMS.txt"
    out.write_text("".join(f"{v}  {k}\n" for k,v in sorted(entries.items())),encoding="utf8")
    print("ATT_A_SHA256_LEDGER "+str(out)+" files="+str(len(entries)))
    for k,v in sorted(entries.items()): print("RAW_SHA256 "+v+" "+k)

if __name__=="__main__":
    result=unittest.main(argv=[sys.argv[0]],verbosity=2,exit=False)
    if not result.result.wasSuccessful(): sys.exit(1)
    ledger()
