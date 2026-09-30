#!/usr/bin/env bash
# Fetch raw reads for a GEO series accession.
# Usage: bash data/fetch_data.sh GSE201842
# Resolves GSE -> SRA run accessions via entrez-direct, then
# downloads with prefetch and converts to FASTQ with fasterq-dump.
set -euo pipefail

GSE="${1:?usage: bash data/fetch_data.sh <GSE_accession>}"
OUT="data/raw/${GSE}"
mkdir -p "${OUT}"

echo "Resolving ${GSE} -> SRA runs..."
esearch -db sra -query "${GSE}" \
  | efetch -format runinfo \
  | cut -d, -f1 \
  | grep -E '^(SRR|ERR|DRR)' \
  | sort -u > "${OUT}/runs.txt"

N=$(wc -l < "${OUT}/runs.txt")
echo "Found ${N} runs. Downloading to ${OUT}/ ..."
while read -r RUN; do
  echo "--- ${RUN}"
  prefetch "${RUN}" -O "${OUT}"
  fasterq-dump "${OUT}/${RUN}" -O "${OUT}" --split-files --skip-technical
  gzip -f "${OUT}/${RUN}"_*.fastq
done < "${OUT}/runs.txt"

echo "Done. FASTQs in ${OUT}/ ; run list in ${OUT}/runs.txt"
