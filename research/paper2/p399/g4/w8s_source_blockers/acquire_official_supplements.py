#!/usr/bin/env python3
import hashlib, json, pathlib, subprocess, urllib.parse, urllib.request
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
TXT = ROOT / "extracted_text_non_authority"
RAW.mkdir(parents=True, exist_ok=True)
TXT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("BLF-02","10.1371/journal.pcbi.1006972","10.1371/journal.pcbi.1006972.s005","S1 File"),
    ("MEM-03","10.1371/journal.pcbi.1004003","10.1371/journal.pcbi.1004003.s001","S1 Text"),
    ("SKL-01","10.1371/journal.pcbi.1012455","10.1371/journal.pcbi.1012455.s001","S1 File"),
    ("SKL-03","10.1371/journal.pcbi.1006839","10.1371/journal.pcbi.1006839.s002","S2 Data"),
    ("SKL-03","10.1371/journal.pcbi.1006839","10.1371/journal.pcbi.1006839.s003","S3 Data"),
    ("INT-07","10.1371/journal.pcbi.1003383","10.1371/journal.pcbi.1003383.s001","Text S1"),
    ("INT-07","10.1371/journal.pcbi.1003383","10.1371/journal.pcbi.1003383.s002","Text S2"),
    ("INT-07","10.1371/journal.pcbi.1003383","10.1371/journal.pcbi.1003383.s003","Text S3"),
    ("INT-07","10.1371/journal.pcbi.1003383","10.1371/journal.pcbi.1003383.s004","Text S4"),
]

receipts = []
for paper_id, publication_doi, supplement_doi, label in TARGETS:
    encoded = urllib.parse.quote(supplement_doi, safe=".")
    url = f"https://journals.plos.org/ploscompbiol/article/file?id={encoded}&type=supplementary"
    out = RAW / f"{paper_id}_{supplement_doi.rsplit('.',1)[-1]}.pdf"
    rec = {
        "paper_id": paper_id,
        "publication_doi": publication_doi,
        "supplement_identifier": supplement_doi,
        "publisher_label": label,
        "source_url": url,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "retrieval_provenance": "GitHub Actions HTTPS GET from official PLOS Computational Biology supplementary endpoint; redirects followed; raw response bytes written unchanged.",
        "status": "ERROR",
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"RelayTheory-W8S/1.0 (+https://github.com/rinsakamo/relay-theory)"})
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
            final_url = r.geturl()
            ctype = r.headers.get("Content-Type")
        if not data.startswith(b"%PDF-"):
            raise RuntimeError(f"non-PDF payload: prefix={data[:16]!r}")
        out.write_bytes(data)
        rec.update({
            "status":"ACQUIRED",
            "mime":ctype,
            "file_type":"PDF",
            "byte_length":len(data),
            "sha256":hashlib.sha256(data).hexdigest(),
            "raw_repository_path":str(out.relative_to(ROOT.parent.parent.parent.parent.parent.parent)).replace("\\","/") if False else f"research/paper2/p399/g4/w8s_source_blockers/raw/{out.name}",
            "final_redirect_host":urllib.parse.urlparse(final_url).netloc,
            "final_redirect_path":urllib.parse.urlparse(final_url).path,
        })
        txt = TXT / (out.stem + ".txt")
        try:
            subprocess.run(["pdftotext","-layout",str(out),str(txt)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            rec["derived_text_repository_path"] = f"research/paper2/p399/g4/w8s_source_blockers/extracted_text_non_authority/{txt.name}"
            rec["derived_text_authority"] = False
        except Exception as e:
            rec["derived_text_error"] = repr(e)
    except Exception as e:
        rec["error"] = repr(e)
    receipts.append(rec)

payload = {
    "schema":"relaytheory.p399.g4.w8s.official_supplement_acquisition_receipts.pre_audit_v1",
    "authority":{"issue":399,"w7_frozen_head":"4325a9a4cba4da651e7cdf2617f7bc8b08c90f54"},
    "exact_target_count":5,
    "required_supplement_count":9,
    "receipts":receipts,
    "all_raw_acquired":all(r["status"]=="ACQUIRED" for r in receipts),
    "raw_acquired_count":sum(r["status"]=="ACQUIRED" for r in receipts),
    "note":"Derived text is convenience-only and is never a substitute for frozen raw publisher bytes."
}
(ROOT/"W8S_ACQUISITION_RECEIPTS_PREAUDIT_v1.json").write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(payload,indent=2,ensure_ascii=False))
