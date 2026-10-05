#!/usr/bin/env python3
"""Independent prepublication original author code source check, fail closed."""
import argparse,csv,hashlib,io,json,subprocess,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=json.loads((HERE/"PRD01_PREPUBLICATION_TASK_CODE_NUMERIC_RECONCILIATION_DELTA_v1.json").read_text())
PARENT="29fb9f96d5990c1b06e562eaf5e5dd370d1a34f9"
COMMIT="ab131a9d0366df00ac2dc79438fe9a89e30f5767"
def audit_metadata(d):
    assert d["schema"]=="relaytheory.p399.g2.prd01.studies2_4_original_code_numeric_reconciliation_delta.v1"
    au=d["authority"]; ev=d["frozen_native_code_evidence"]; dist=d["sample_distribution"]; disp=d["authoritative_interpretation"]; con=d["publication_conflicts_still_visible"]
    assert au["author_public_release_commit"]==COMMIT
    assert au["recorded_git_author_date_utc"]=="2024-05-04T15:49:57Z"
    assert au["publisher_main_first_publication"]=="2024-07-16"
    assert ev["study2"]["training_csv"]["git_blob_sha"]=="6e6e016a53dea8b02e8f4d8fed7de0dc8b4da0b3"
    assert ev["study4"]["training_csv"]["git_blob_sha"]=="5e9bffe4697f8c469758c6fe93df5705c406c261"
    assert ev["study2"]["load_runtime"]["git_blob_sha"]=="f5a9d5989ff48d562ebecbeadd36e8c7dcdb935a"
    assert ev["study4"]["load_runtime"][0]["git_blob_sha"]=="4fec9b42cd827b5a7f8375744c0ff155d072c3ca"
    for s in ("study2","study4"):
        x=ev[s]["training_csv"]
        assert (x["rows"],x["trident_rows"],x["planet_rows"])==(520,360,160)
    assert (dist["n"],dist["trident_count"],dist["planet_count"])==(520,360,160)
    assert dist["rounded_main_official_corrected"]=={"trident":0.69,"planet":0.31}
    assert con["published_supplement_figS2_study2_diagram"]=={"trident":0.33,"planet":0.67}
    assert con["published_supplement_figS2_study2_caption"]=={"trident":0.67,"planet":0.33}
    assert con["official_notice_and_author_approved_manuscript_main_study2_and_study4"]=={"trident":0.69,"planet":0.31}
    assert con["missing_official_supplement_figS2_correction_notice"] is True
    assert con["no_silent_backpatch_of_published_supplement"] is True
    assert disp["intended_public_prepublication_experiment_study2_study4_task_base_frequencies"]=="STRONGLY_CORROBORATED_360_160_BY_RELEASED_PREPUBLICATION_CODE_AND_MAIN_CORRECTION"
    assert disp["published_supplement_figS2_documentary_equivalence"]=="FAIL_INTERNALLY_CONTRADICTORY_UNCORRECTED"
    assert disp["exact_historical_each_participant_delivered_trials_from_permanent_empirical_logs"]=="NOT_EXAMINED"
    assert disp["full_PRD01_admission"] is False
    assert disp["family_independence"] is False
    assert disp["G2_partial"] is True
    assert disp["main_authorized"] is False
audit_metadata(D)
assert subprocess.check_output(["git","rev-parse","HEAD:research/paper2/p399/g2/supplement_20261005/THREE_SUPPLEMENT_EXACT_SOURCE_AND_SCIENCE_RECEIPT_v1.json"],text=True).strip()==PARENT
print("PASS source pinned May-2024 code-design scope and contradictory published Figure S2 retained")
# Fourteenth failure guards are semantic metadata, not same as physical GitHub code independent fetch
import copy
mods=[
 lambda x:x["authoritative_interpretation"].update(published_supplement_figS2_documentary_equivalence="CLEARED"),
 lambda x:x["authoritative_interpretation"].update(exact_historical_each_participant_delivered_trials_from_permanent_empirical_logs="PROVEN"),
 lambda x:x["authoritative_interpretation"].update(full_PRD01_admission=True),
 lambda x:x["authoritative_interpretation"].update(main_authorized=True),
 lambda x:x["publication_conflicts_still_visible"].update(no_silent_backpatch_of_published_supplement=False),
 lambda x:x["publication_conflicts_still_visible"].update(published_supplement_figS2_study2_diagram={"trident":.69,"planet":.31}),
 lambda x:x["sample_distribution"].update(trident_count=160),
 lambda x:x["frozen_native_code_evidence"]["study2"]["training_csv"].update(git_blob_sha="0"*40)]
for n,m in enumerate(mods):
    c=copy.deepcopy(D);m(c)
    try:audit_metadata(c)
    except AssertionError:continue
    raise AssertionError(f"false paper-code promotion {n} passed")
print(f"PASS {len(mods)}/{len(mods)} code-figure false promotion mutations rejected")
def remote_check(path,sha, kind, expect_ref=None):
    url="https://raw.githubusercontent.com/psharp1289/Humans-Adaptively-Deploy-Forward-and-Backward-Prediction/"+COMMIT+"/"+path
    q=urllib.request.Request(url,headers={"User-Agent":"RelayTheorySourceVerifier/1"})
    with urllib.request.urlopen(q,timeout=15) as o:b=o.read(900000)
    git_blob=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert git_blob==sha,(path,git_blob,sha)
    s=b.decode("utf-8-sig")
    if kind=="csv":
        rr=list(csv.DictReader(io.StringIO(s)))
        counts={}
        for row in rr:
            k=row["s1_image"]
            counts[k]=counts.get(k,0)+1
        assert len(rr)==520 and counts=={"trident.png":360,"planet.png":160},(path,len(rr),counts)
        print("PASS prepublication source task exact Git blob",path,"520/360/160=0.692307/0.307692")
    else:
        assert ("trialList: '"+expect_ref+"'") in s,(path,expect_ref)
        print("PASS prepublication exact original task JS loads",path,expect_ref)
ap=argparse.ArgumentParser();ap.add_argument("--remote",action="store_true");args=ap.parse_args()
if args.remote:
    e=D["frozen_native_code_evidence"]
    for key in ["study2","study4"]:
        train=e[key]["training_csv"]
        remote_check(train["path"],train["git_blob_sha"],"csv")
        runners=e[key]["load_runtime"]
        if not isinstance(runners,list):runners=[runners]
        for rt in runners[:1]:
            remote_check(rt["path"],rt["git_blob_sha"],"js",rt["references_trialList"])
    print("PASS 4/4 prepublication CSV and runtime JS original Git SHA + 2x520 original native trial counts")
else:print("SKIP independent remote source fetch; use --remote on networked runner")
