# PRC1 in the Drosophila Female Germline

Reanalysis of public ChIP-seq and RNA-seq data to map where Polycomb
Repressive Complex 1 (PRC1) binds in the *Drosophila* female germline and
what happens transcriptionally when Polycomb repression is lost.

**Question.** Which genes does PRC1 occupy in ovaries / germline stem cells,
and which of those genes are derepressed when Polycomb silencing is removed?

This project is fully reproducible from public data — no private datasets required.

## Datasets

| # | Data | Tissue | Accession |
|---|------|--------|-----------|
| 1 | BioTAP ChIP-seq: Jarid2, Pcl (PRC2 accessory subunits) — pipeline test, embryonic reference | 12–24 h embryos | `GSE201842` |
| 2 | ChIP-seq on sorted germ cells: Ph (PRC1), Pho, H3K27me3 across GSC → nurse cell | ovary germline | `GSE145282` |
| 3 | RNA-seq after germline knockdown of Sce, Pc, Scm (PRC1) and E(z), Pcl, Jarid2 (PRC2) | ovary | `GSE145282` |

Verified run accessions are in `data/accessions.tsv`. Raw reads are **not**
stored in this repo; `data/fetch_data.sh` downloads them from SRA.

## Pipeline

```
GSE accession
    │  data/fetch_data.sh  (entrez-direct → prefetch → fasterq-dump)
    ▼
FASTQ ──► FastQC / fastp ──► Bowtie2 (dm6) ──► MACS2 peak calling ──► annotated peaks
                                 │
                                 └─► STAR (dm6) ──► featureCounts ──► PyDESeq2 ──► DE genes
                                                                            │
                                              ┌───────────────────────────────┘
                                              ▼
                                   peak–gene overlap, GO enrichment (gseapy),
                                   heatmaps / genome tracks (matplotlib)
                                              │
                                              ▼ (optional extension)
                                   sklearn classifier: predict PRC1-bound
                                   promoters from k-mer sequence features
```

## Reproduce

```bash
# 1. environment (mamba recommended)
mamba env create -f env.yml && conda activate prc1-germline

# 2. fetch one dataset (example)
bash data/fetch_data.sh GSE201842

# 3. run the workflow (dry-run first)
snakemake -n
snakemake --cores 8
```

## Repo layout

```
data/           accession lists, fetch script (raw reads live here, git-ignored)
workflow/       Snakefile + config
scripts/        peak annotation, integration, ML extension
notebooks/      exploratory analysis
results/        peaks, counts, DE tables, figures (git-ignored)
```

## Roadmap

- [ ] Fetch + QC all four datasets
- [ ] PRC1 peak sets (MACS2, replicate-consensus)
- [ ] Differential expression (Polycomb-depleted vs control ovaries)
- [ ] Peak–DE-gene overlap + GO enrichment
- [ ] Figures: peak distribution, MA plot, signal heatmaps
- [ ] (stretch) k-mer classifier for PRC1 binding
