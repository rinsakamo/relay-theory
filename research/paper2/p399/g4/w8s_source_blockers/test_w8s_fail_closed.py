#!/usr/bin/env python3
import copy, hashlib, json, pathlib, re, unittest

ROOT=pathlib.Path(__file__).resolve().parent
FREEZE=json.loads((ROOT/"W8S_OFFICIAL_SUPPLEMENT_FREEZE_v1.json").read_text())
RES=json.loads((ROOT/"W8S_FIVE_PROFILE_RESOLUTION_v1.json").read_text())
IMP=json.loads((ROOT/"W8S_PROFILE_IMPORT_FRAGMENTS_v1.json").read_text())
CON=json.loads((ROOT/"W8S_SOURCE_CONFLICTS_AND_REMAINING_BLOCKERS_v1.json").read_text())

EXPECTED_DOIS={
 "BLF-02":"10.1371/journal.pcbi.1006972",
 "MEM-03":"10.1371/journal.pcbi.1004003",
 "SKL-01":"10.1371/journal.pcbi.1012455",
 "SKL-03":"10.1371/journal.pcbi.1006839",
 "INT-07":"10.1371/journal.pcbi.1003383",
}
EXPECTED_SUPPS={
 "BLF-02":{"10.1371/journal.pcbi.1006972.s005"},
 "MEM-03":{"10.1371/journal.pcbi.1004003.s001"},
 "SKL-01":{"10.1371/journal.pcbi.1012455.s001"},
 "SKL-03":{"10.1371/journal.pcbi.1006839.s002","10.1371/journal.pcbi.1006839.s003"},
 "INT-07":{"10.1371/journal.pcbi.1003383.s001","10.1371/journal.pcbi.1003383.s002","10.1371/journal.pcbi.1003383.s003","10.1371/journal.pcbi.1003383.s004"},
}
HEX64=re.compile(r"^[0-9a-f]{64}$")

def validate(freeze,res):
    assert freeze["exact_publication_dois"]==EXPECTED_DOIS
    assert {k:set(v) for k,v in freeze["exact_required_supplements"].items()}==EXPECTED_SUPPS
    receipts={r["supplement_identifier"]:r for r in freeze["receipts"]}
    papers={p["id"]:p for p in res["papers"]}
    assert set(papers)==set(EXPECTED_DOIS)
    for pid,doi in EXPECTED_DOIS.items():
        p=papers[pid]
        assert p["doi"]==doi
        if p["status"]=="PROFILE_FRAGMENT_READY":
            for sid in EXPECTED_SUPPS[pid]:
                assert sid in receipts, (pid,sid)
                r=receipts[sid]
                assert r["raw_bytes_frozen"] is True
                assert HEX64.match(r["sha256"])
                raw=ROOT.parents[0] / pathlib.Path(r["raw_repository_path"]).relative_to("research/paper2/p399/g4/w8s_source_blockers")
                assert raw.exists(), raw
                assert hashlib.sha256(raw.read_bytes()).hexdigest()==r["sha256"]
    return True

class W8SFailClosed(unittest.TestCase):
    def test_current_bundle(self): self.assertTrue(validate(FREEZE,RES))
    def test_exact_five_dois(self): self.assertEqual(FREEZE["exact_publication_dois"],EXPECTED_DOIS)
    def test_exact_required_supplements(self): self.assertEqual({k:set(v) for k,v in FREEZE["exact_required_supplements"].items()},EXPECTED_SUPPS)
    def test_sha_and_raw_bytes_recomputed(self):
        for r in FREEZE["receipts"]:
            self.assertRegex(r["sha256"],HEX64)
            raw=ROOT / pathlib.Path(r["raw_repository_path"]).relative_to("research/paper2/p399/g4/w8s_source_blockers")
            self.assertTrue(raw.exists())
            self.assertEqual(hashlib.sha256(raw.read_bytes()).hexdigest(),r["sha256"])
    def test_ready_fails_if_mandatory_missing(self):
        f=copy.deepcopy(FREEZE); f["receipts"]=f["receipts"][1:]
        with self.assertRaises(AssertionError): validate(f,RES)
    def test_skl03_two_of_two_required(self):
        f=copy.deepcopy(FREEZE); f["receipts"]=[r for r in f["receipts"] if r["supplement_identifier"]!="10.1371/journal.pcbi.1006839.s003"]
        with self.assertRaises(AssertionError): validate(f,RES)
    def test_int07_four_of_four_required(self):
        for sid in EXPECTED_SUPPS["INT-07"]:
            f=copy.deepcopy(FREEZE); f["receipts"]=[r for r in f["receipts"] if r["supplement_identifier"]!=sid]
            with self.assertRaises(AssertionError): validate(f,RES)
    def test_no_source_substitution(self):
        self.assertFalse(FREEZE["source_substitution_used"])
        self.assertFalse(FREEZE["mirror_only_rehost_used"])
        for r in FREEZE["receipts"]:
            self.assertTrue(r["source_url"].startswith("https://journals.plos.org/ploscompbiol/article/file?"))
            self.assertEqual(r["publisher_redirect_provenance"]["host"],"storage.googleapis.com")
    def test_no_global_independence_or_main_authorization(self):
        for obj in (RES,IMP,CON):
            self.assertIs(obj.get("global_family_independence_certified"),False)
            self.assertIs(obj.get("main_authorized"),False)
        for p in IMP["import_fragments"]:
            self.assertIs(p["global_family_independence_certified"],False)
    def test_only_ready_imported(self):
        ready={p["id"] for p in RES["papers"] if p["status"]=="PROFILE_FRAGMENT_READY"}
        self.assertEqual({p["id"] for p in IMP["import_fragments"]},ready)
        self.assertEqual(IMP["import_count"],len(ready))
    def test_shared_science_untouched(self):
        self.assertFalse(IMP["shared_w7_registry_directly_modified"])
        self.assertFalse(IMP["pair_matrix_scientific_decisions_modified"])
        self.assertFalse(CON["g1_genealogy_modified"])
        self.assertFalse(CON["grammar_v0_modified"])
        self.assertFalse(CON["h0_h1_h2_modified"])
        self.assertFalse(CON["main_science_modified"])

if __name__=="__main__": unittest.main()
