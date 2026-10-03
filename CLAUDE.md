# prc1-germline — assistant context

## Project
Reanalysis of public *Drosophila* ChIP-seq and RNA-seq data: map where PRC1
binds in the female germline and which genes are derepressed when Polycomb
silencing is lost. Fully reproducible from public data (see README.md).

## Who's driving
Soham — UCR undergrad (Neuroscience B.S., Data Science minor).
Strong Python (pandas, scikit-learn, matplotlib). Wet-lab *Drosophila*
geneticist (PRC1/Sce crosses, dissections, imaging).
New to bioinformatics CLI tooling: conda envs, read aligners, genome builds,
peak callers. This is his first computational genomics project.

## How to help
- Teach, don't just dump code. Before each new tool or concept, explain the
  *why* in 1–2 sentences (e.g., what a BAM file is, why we trim reads, what
  MACS2 is actually doing).
- Small steps. One pipeline stage at a time; verify outputs (file exists,
  read counts, peak numbers) before moving on.
- Prefer Python where reasonable (pandas, pyranges, pydeseq2, matplotlib);
  use standard CLI tools where they're the norm (bowtie2, STAR, MACS2, samtools).
- First time a flag appears, say what it does. Don't re-explain after that.
- If a step can fail silently (empty BAM, zero peaks), add the sanity check.
- Keep answers tight; he's technical and prefers brevity.

## Environment
- Toolchain: `env.yml` (mamba/conda, conda-forge + bioconda channels)
- Reference genome: *Drosophila* dm6 — FASTA/GTF download source TBD,
  record the exact URLs in `config/config.yaml` once chosen
- Machine (checked 2026-10-03): Windows 11 Home, 8 cores, 16 GB RAM.
  Everything runs in WSL2 Ubuntu 26.04 (bioconda tools are Linux-only).
  - Ubuntu's disk lives at `D:\WSL\Ubuntu` (C: is nearly full). D: is a
    spinning HDD: I/O-heavy steps will be slower than on SSD.
  - Repo, raw data and results all live inside Linux at `~/prc1-germline`;
    avoid `/mnt/c` / `/mnt/d` for pipeline I/O (slow).
  - Free space on D: ~136 GB. ChIP-seq + RNA-seq needs ~50–100 GB scratch;
    confirm before fetching.
  - WSL gets 7 GB RAM by default — enough for a dm6 STAR index (~2–3 GB).
  - Miniforge at `~/miniforge3`; env `prc1-germline` (~4 GB), activate with
    `conda activate prc1-germline`.

## Data plan (in this order — don't parallelize until step 1 works end to end)
1. `GSE201842` — BioTAP ChIP-seq (Jarid2, Pcl). Start here.
2. `GSE66183` — BioTAP ChIP-seq (E(z), Scm).
3. modENCODE Pc/Ph developmental ChIP data.
4. Ovary RNA-seq (Polycomb-depleted vs control) — accessions TBD, see
   `data/accessions.tsv`.

## Conventions
- Raw reads live in `data/raw/` (git-ignored). Never commit them.
- Reusable logic in `scripts/`; exploration in `notebooks/`.
- Results in `results/` (git-ignored); only curated figures/tables get
  committed, under `results/` only if small — otherwise describe in README.
- Snakemake orchestrates; `config/config.yaml` is the single source of truth
  for samples and reference paths.
- Commit small, imperative messages, e.g. "call peaks for Jarid2 rep1".
