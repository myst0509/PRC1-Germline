#!/usr/bin/env bash
# Download raw reads for the verified runs listed in data/accessions.tsv.
# Usage: bash data/fetch_data.sh <dataset> [run]
#   bash data/fetch_data.sh GSE201842               # every run in the dataset
#   bash data/fetch_data.sh GSE201842 SRR18970068   # one run (good for testing)
# Writes data/raw/<dataset>/<run>.fastq.gz; finished runs are skipped.
set -euo pipefail

DATASET="${1:?usage: bash data/fetch_data.sh <dataset> [run]}"
ONLY="${2:-}"
OUT="data/raw/${DATASET}"
THREADS="${THREADS:-4}"
mkdir -p "${OUT}"

mapfile -t RUNS < <(awk -F'\t' -v d="${DATASET}" -v r="${ONLY}" \
  '!/^#/ && $1 == d && (r == "" || $3 == r) {print $3}' data/accessions.tsv)
if [ "${#RUNS[@]}" -eq 0 ]; then
  echo "ERROR: no runs for '${DATASET}' ${ONLY} in data/accessions.tsv" >&2
  exit 1
fi
echo "${#RUNS[@]} run(s) for ${DATASET} -> ${OUT}/"

for RUN in "${RUNS[@]}"; do
  FQ="${OUT}/${RUN}.fastq.gz"
  if [ -s "${FQ}" ]; then
    echo "--- ${RUN}: already done, skipping"
    continue
  fi
  echo "--- ${RUN}"
  prefetch "${RUN}" -O "${OUT}"
  fasterq-dump "${OUT}/${RUN}" -O "${OUT}" -t "${OUT}" -e "${THREADS}" --skip-technical
  rm -rf "${OUT:?}/${RUN}"   # the .sra is no longer needed once converted

  # Single-end runs give <run>.fastq; anything else means the layout isn't what we expect
  if [ ! -s "${OUT}/${RUN}.fastq" ]; then
    echo "ERROR: ${RUN}: expected single-end ${OUT}/${RUN}.fastq; got:" >&2
    ls "${OUT}/${RUN}"* >&2 || true
    exit 1
  fi
  LINES=$(wc -l < "${OUT}/${RUN}.fastq")
  if [ $((LINES % 4)) -ne 0 ]; then
    echo "ERROR: ${RUN}: ${LINES} lines is not a multiple of 4 (truncated FASTQ?)" >&2
    exit 1
  fi
  gzip "${OUT}/${RUN}.fastq"
  echo "    ${RUN}: $((LINES / 4)) reads"
done

echo "Done."
