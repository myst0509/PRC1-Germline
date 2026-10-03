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
1. `GSE201842` — BioTAP ChIP-seq (Jarid2, Pcl), **12–24 h embryos**, not
   germline. Pipeline test + embryonic reference. Start here.
2. `GSE145282` ChIP (PMID 32773039) — sorted germ cells: Ph (PRC1) in GSC
   and ovary, Pho in GSC, H3K27me3 GSC → 2C → 16C → NC. Mostly single
   replicates; one GSC Ph sort is in a Pcl-GLKD background.
3. `GSE145282` RNA-seq — germline KD of Sce, Pc, Scm (PRC1), E(z), Pcl,
   Jarid2 (PRC2) vs Luc/w controls, 3 reps each.
4. Integrate: Ph-bound genes ∩ genes derepressed on Sce/Pc/Scm GLKD.
5. Optional: `GSE176034` (Sfmbt GLKD RNA-seq + Pho ChIP, ovary) for
   recruitment; `GSE174250` / `GSE250350` / `GSE335290` H3K27me3 to check
   replication across labs.
- Dropped `GSE66183` (embryo/S2) and modENCODE (whole animal): no germline
  data and redundant with step 1.
- Known gap (GEO search 2026-10-03): no Sce, Psc or H2Aub profiling in
  ovary/GSC — germline PRC1 occupancy is only measurable via Ph.

## Conventions
- Raw reads live in `data/raw/` (git-ignored). Never commit them.
- Reusable logic in `scripts/`; exploration in `notebooks/`.
- Results in `results/` (git-ignored); only curated figures/tables get
  committed, under `results/` only if small — otherwise describe in README.
- Snakemake orchestrates; `config/config.yaml` is the single source of truth
  for samples and reference paths.
- Commit small, imperative messages, e.g. "call peaks for Jarid2 rep1".
