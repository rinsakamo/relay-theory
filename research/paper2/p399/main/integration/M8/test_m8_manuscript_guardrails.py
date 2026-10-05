#!/usr/bin/env python3
import json, re, subprocess
from pathlib import Path

R = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git","rev-parse","--show-toplevel"], text=True).strip())
BASE = "48b2cf3c627e030e7131af485206b0013d7e02f1"
MAIN = (ROOT/"paper/venues/jgps/main.tex").read_text()
CHECKLIST = (ROOT/"paper/venues/jgps/submission-checklist.md").read_text()
COVER = (ROOT/"paper/venues/jgps/cover-letter.md").read_text()
REC = json.loads((R/"M8_MANUSCRIPT_INTEGRATION_RECEIPT_v1.json").read_text())
BOUND = json.loads((R/"M8_CLAIM_BOUNDARY_v1.json").read_text())
M7 = json.loads((ROOT/"research/paper2/p399/main/integration/M7/M7_MAIN_SCIENTIFIC_ADJUDICATION_v1.json").read_text())
GEN = json.loads((ROOT/"research/paper2/p399/main/integration/M7/M7_GENEALOGY_AWARE_MAIN_SUMMARY_v1.json").read_text())
OLD = json.loads((ROOT/"research/paper2/designed_source_manifest_v1.json").read_text())
NEW = json.loads((ROOT/"research/paper2/p399/g2/MAIN40_G2_ADMISSION_WORKING_MANIFEST_v5.json").read_text())

checks=[]
def ck(name, cond):
    if not cond: raise AssertionError(name)
    checks.append(name); print(f"PASS {len(checks):02d} {name}")

m=re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",MAIN,re.S)
words=re.findall(r"\b[A-Za-z0-9][A-Za-z0-9'/-]*\b",m.group(1))
old_dois={str(e.get("stable_identity",{}).get("value","")).lower() for e in OLD["entries"]}
new_rows=NEW.get("selected_working_roster",[])
new_dois={str(e.get("doi","")).lower() for e in new_rows}
changed=subprocess.check_output(["git","diff","--name-only",BASE+"...HEAD"],text=True).splitlines()
allowed=lambda p: p in {"paper/venues/jgps/main.tex","paper/venues/jgps/cover-letter.md","paper/venues/jgps/submission-checklist.md",".github/workflows/p399-main-m8-jgps-integration.yml"} or p.startswith("research/paper2/p399/main/integration/M8/")

ck("01 base M7 authority exact",REC["base_m7_head"]==BASE)
ck("02 M7 certified exact MAIN40",M7["status"]=="CERTIFIED_EXACT_MAIN40_SCIENTIFIC_RESULT")
ck("03 A0 exact 40",M7["m7_accepted_state_counts"]["A0_FIDELITY"]==40)
ck("04 A1 zero",M7["m7_accepted_state_counts"]["A1_FIDELITY"]==0)
ck("05 A2 zero",M7["m7_accepted_state_counts"]["A2_FIDELITY"]==0)
ck("06 component 24/24",M7["accepted_arm_counts"]["component"]["A0_FIDELITY"]==24)
ck("07 integrated 16/16",M7["accepted_arm_counts"]["integrated"]["A0_FIDELITY"]==16)
ck("08 exact DOI overlap zero",len(old_dois & new_dois)==0 and REC["corpus_relation"]["exact_doi_overlap"]==0)
ck("09 MAIN40 roster exact 40",len(new_dois)==40)
ck("10 abstract 150-250 words",150<=len(words)<=250)
ck("11 original whole-claim failure preserved","1770/1770" in MAIN)
ck("12 bounded reconstruction preserved","206 unique" in MAIN and "99 cross-lane families" in MAIN)
ck("13 role-gap result preserved","ROLE\\_GAP}=0" in MAIN)
ck("14 prospective methods present","Prospective mechanism-composition validation" in MAIN)
ck("15 prospective results present","Prospective composition test: 40/40 direct reconstruction" in MAIN)
ck("16 exact arm counts stated","24/24" in MAIN and "16/16" in MAIN)
ck("17 source-defined state not double-counted","does not say that stateful coordination is absent" in MAIN)
ck("18 genealogy raw counts match",GEN["main40_pair_denominator"]==780 and REC["genealogy"]["UNDERDETERMINED"]==670 and REC["genealogy"]["SHARED_CONSTITUENT_ONLY"]==25)
ck("19 no independence promotion","not as 40 independent statistical replications" in MAIN and REC["genealogy"]["global_independence_claimed"] is False)
ck("20 no binomial promotion","naive binomial inference" in MAIN)
ck("21 global H remains insufficient",BOUND["overall_hypothesis_status"]=="INSUFFICIENT_FOR_GLOBAL_H_DISCRIMINATION" and "universal falsification" in MAIN)
ck("22 M7 receipt exposed","48b2cf3c627e030e7131af485206b0013d7e02f1" in MAIN and "37297573776" in MAIN)
ck("23 title unchanged","Toward a Construct-Label-Neutral Structural Comparison Basis for Cognitive Capacities" in MAIN)
ck("24 package-facing prose updated","Prospective MAIN40 composition extension" in CHECKLIST and "40 source-native cognitive-model papers" in COVER)
ck("25 M8 isolation",all(allowed(p) for p in changed) and not any("/M7/" in p for p in changed))
print(f"M8_MANUSCRIPT_GUARD_PASS {len(checks)}/{len(checks)}")
