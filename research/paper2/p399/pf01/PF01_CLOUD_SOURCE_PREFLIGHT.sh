#!/usr/bin/env bash
# PF01 SOURCE-ONLY CLOUD PREFLIGHT. Never grant scientific PRE_A qualification automatically.
# CC-BY source files, if fetched, remain ephemeral on the runner and are NEVER git committed.
set -uo pipefail
ROOT="${RUNNER_TEMP:-/tmp}/pf01_source_preflight"
mkdir -p "$ROOT"/{private,output}
META="$ROOT/output/run_log.txt"
exec > >(tee -a "$META") 2>&1
printf '%s\n' "PF01_PRE_A_CLOUD_SOURCE_ONLY=1" "UTC_TIME=$(date -u +%FT%TZ)"
printf '%s\n' "PUBLISHER_SOURCE=https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006928&type=printable"
printf '%s\n' "AUTHOR_INSTITUTION=https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/Seeholzer19.pdf"
if ! command -v pdfinfo >/dev/null || ! command -v pdftoppm >/dev/null; then
  sudo apt-get -qq update && sudo apt-get -y -qq install poppler-utils || echo "POPPLER_UNAVAILABLE"
fi
for kind in PUBLISHER AUTHOR_INSTITUTION; do
  if [ "$kind" = PUBLISHER ]; then
    URL='https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1006928&type=printable'
  else
    URL='https://lcnwww.epfl.ch/gerstner/PUBLICATIONS/Seeholzer19.pdf'
  fi
  DEST="$ROOT/private/$kind.pdf"
  echo "BEGIN_ATTEMPT=$kind"
  curl --fail --location --silent --show-error --retry 1 --retry-delay 2 --connect-timeout 10 --max-time 60 --user-agent 'RelayTheory PF01 source qualification (academic; one-shot)' --output "$DEST" "$URL"
  STATUS=$?
  echo "CURL_EXIT_$kind=$STATUS"
  if [ "$STATUS" -eq 0 ] && [ -s "$DEST" ] && [ "$(head -c 4 "$DEST")" = '%PDF' ]; then
    echo "RAW_PDF_RECEIVED=$kind"
    echo "SOURCE_BYTES_$kind=$(wc -c < "$DEST" | tr -d ' ')"
    echo "SOURCE_SHA256_$kind=$(sha256sum "$DEST" | cut -d' ' -f1)"
    pdfinfo "$DEST" | grep -E 'Pages:|PDF version:|Page size:|CreationDate:|ModDate:|Title:' || true
    pdftotext -f 1 -l 2 "$DEST" "$ROOT/output/$kind-title.txt" || true
    if [ "$kind" = PUBLISHER ]; then echo "$kind" > "$ROOT/output/received_medium.txt"; fi
    if command -v pdftoppm >/dev/null; then
      mkdir -p "$ROOT/output/$kind-sample-pages"
      for page in 4 5 6 7 8 19 20 21 22 23 25 30 34; do
        pdfpages=$(pdfinfo "$DEST" | awk '/^Pages:/ {print $2}')
        if [ -n "$pdfpages" ] && [ "$page" -le "$pdfpages" ]; then
          pdftoppm -f "$page" -l "$page" -scale-to 1350 -jpeg -jpegopt quality=76 -singlefile "$DEST" "$ROOT/output/$kind-sample-pages/p$(printf '%02d' "$page")" || true
        fi
      done
      echo "SELECTED_RENDER_COUNT_$kind=$(find "$ROOT/output/$kind-sample-pages" -name '*.jpg' | wc -l)"
    fi
    # Preserve metadata and page images only. Do not add full copyright source PDF to artifact or Git.
    if [ "$kind" = PUBLISHER ]; then break; fi
  else
    echo "NO_VALID_RAW_PDF=$kind"
    rm -f "$DEST"
  fi
  echo "END_ATTEMPT=$kind"
done
if [ ! -f "$ROOT/output/received_medium.txt" ]; then
  echo "PUBLISHER_PDF_NOT_BYTE_VERIFIED"
  echo "If author-host PDF was obtained it remains SECONDARY until exact-edition check."
fi
echo "NO_AUTOMATIC_PRE_A_PASS"
