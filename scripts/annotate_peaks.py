"""Annotate MACS2 peaks to nearest genes and overlap with DE results.

Usage (via snakemake) or standalone:
    python scripts/annotate_peaks.py --peaks results/peaks/Jarid2_rep1_peaks.narrowPeak \
        --gtf data/ref/dm6.gtf --de results/rna/deseq2_results.tsv \
        --out results/integration/peak_gene_overlap.tsv
"""
import argparse

import pandas as pd
import pyranges as pr


def load_peaks(path: str) -> pr.PyRanges:
    cols = ["Chromosome", "Start", "End", "name", "score", "strand",
            "signalValue", "pValue", "qValue", "peak"]
    df = pd.read_csv(path, sep="\t", header=None, names=cols,
                     usecols=["Chromosome", "Start", "End", "name", "qValue"])
    return pr.PyRanges(df)


def load_tss(gtf_path: str) -> pr.PyRanges:
    # TODO: point at your dm6 GTF; takes the TSS of each gene
    rows = []
    with open(gtf_path) as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            chrom, _, feat, start, end, _, strand, _, attrs = line.rstrip().split("\t")
            if feat != "gene":
                continue
            gene = [a.split('"')[1] for a in attrs.split(";")
                    if "gene_name" in a or "gene_id" in a][0]
            tss = int(start) if strand == "+" else int(end)
            rows.append((chrom, tss - 1, tss, gene, strand))
    df = pd.DataFrame(rows, columns=["Chromosome", "Start", "End", "gene", "Strand"])
    return pr.PyRanges(df)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--peaks", required=True)
    ap.add_argument("--gtf", required=True)
    ap.add_argument("--de", required=True, help="PyDESeq2 results with gene, padj, log2FoldChange")
    ap.add_argument("--out", required=True)
    ap.add_argument("--window", type=int, default=2000,
                    help="bp around TSS to call a gene 'bound'")
    args = ap.parse_args()

    peaks = load_peaks(args.peaks)
    tss = load_tss(args.gtf).extend(args.window)
    nearest = peaks.join(tss, how="left", suffix="_gene")

    de = pd.read_csv(args.de, sep="\t")
    de_sig = de[(de["padj"] < 0.05) & (de["log2FoldChange"].abs() > 1)]

    bound = nearest.df[["Chromosome", "Start", "End", "gene"]].dropna().drop_duplicates()
    merged = bound.merge(de_sig, on="gene", how="inner")
    merged.to_csv(args.out, sep="\t", index=False)
    print(f"{len(merged)} DE genes within {args.window}bp of a PRC1 peak -> {args.out}")


if __name__ == "__main__":
    main()
