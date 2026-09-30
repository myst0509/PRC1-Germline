"""Differential expression with PyDESeq2 (pure Python, no R).

Expects featureCounts output. Infers condition from sample names:
samples containing 'control' -> control, else -> treated.
Rename / extend as needed for your design.
"""
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats


def main() -> None:
    counts = pd.read_csv("results/rna/counts.tsv", sep="\t", comment="#", index_col=0)
    counts = counts.drop(columns=["Chr", "Start", "End", "Strand", "Length"])
    counts.columns = [c.split("/")[-1].replace(".sorted.bam", "") for c in counts.columns]

    meta = pd.DataFrame({
        "condition": ["control" if "control" in c else "treated" for c in counts.columns]
    }, index=counts.columns)

    dds = DeseqDataSet(counts=counts.T, metadata=meta, design="~condition", refit_cooks=True)
    dds.deseq2()
    stats = DeseqStats(dds, contrast=("condition", "treated", "control"))
    stats.summary()
    stats.results_df.assign(gene=stats.results_df.index).to_csv(
        "results/rna/deseq2_results.tsv", sep="\t", index=False)
    print("wrote results/rna/deseq2_results.tsv")


if __name__ == "__main__":
    main()
