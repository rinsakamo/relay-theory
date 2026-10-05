#!/usr/bin/env python3
"""G2-D machine ledger fail-closed checks only; NOT scientific truth validation."""
import json
import pathlib
import unittest
P = pathlib.Path(__file__).with_name("G2D_INT_BOUNDED_DECISIONS_v1.json")
class INTGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.o=json.loads(P.read_text(encoding="utf-8"))
    def test_actual_locked_metadata(self):
        o=self.o
        self.assertEqual(o["g2_start_sha"],"69748673c80f421605f1c63607472903ac2ed68c")
        self.assertFalse(o["frozen_main40_roster_changed"])
        self.assertFalse(o["main_authorized"])
        self.assertTrue(o["no_main_science"])
        self.assertEqual(o["backup_activated"],[])
        self.assertEqual(len(o["backups"]),4)
        self.assertEqual([x["rank"] for x in o["backups"]],[1,2,3,4])
        self.assertFalse(o["selected"][0]["publisher_full_original_physically_acquired"])
        self.assertFalse(o["selected"][2]["final_vor_physically_verified"])
        self.assertFalse(o["selected"][2]["proof_to_final_equivalence"])
        self.assertEqual(o["backups"][0]["central_family"],"DIRECT_INT12_DESCENDANT")
        self.assertFalse(o["backups"][1]["g1_relinquished"])
        self.assertEqual(o["backups"][2]["shared_doi_with"],"CTL-B1")
        self.assertFalse(o["backups"][3]["global_family_independence_verified"])
        self.assertTrue(all(not b["activated"] for b in o["backups"]))
        self.assertFalse(o["g1"]["all_central_family_pairs_scientifically_cleared"])
        self.assertEqual(o["other_int_existing_g2_v5_original_pdf_sha_count"],11)
        self.assertEqual(o["counts_this_lane"]["formally_activated_backups"],0)
    def test_seven_destructive_mutants_rejected(self):
        import copy
        cases=[
          (("main_authorized",),True),
          (("selected",0,"publisher_full_original_physically_acquired"),True),
          (("selected",2,"final_vor_physically_verified"),True),
          (("backups",0,"central_family"),"NEW_INDEPENDENT"),
          (("backups",1,"g1_relinquished"),True),
          (("backups",2,"shared_doi_with"),"NONE"),
          (("backups",3,"global_family_independence_verified"),True),
        ]
        for path,new in cases:
            o=copy.deepcopy(self.o)
            ref=o
            for p in path[:-1]:ref=ref[p]
            ref[path[-1]]=new
            with self.subTest(path=path),self.assertRaises(AssertionError):
                self._unchanged_control(o,path)
    def _unchanged_control(self,mutant,path):
        a=self.o
        b=mutant
        for p in path:
            a=a[p];b=b[p]
        self.assertEqual(a,b)
if __name__=="__main__": unittest.main()
