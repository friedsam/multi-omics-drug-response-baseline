 A Reproducible Baseline for Multi-Omics Drug-Response Prediction

**Goal.** Provide a clean, end-to-end baseline pipeline and API scaffold for predicting drug response from multi-omics data, with explicit stress-tests for **missing modalities**.

## Why this repo
- Most “SOTA” papers are hard to reproduce. This is a **usable starting point** others can extend.
- Focus on **robustness**: how badly do models degrade as modalities go missing, and which simple strategies help?

## What’s included
- Minimal FastAPI service (`/predict`) and Dockerfile
- Experiment matrix (`configs/experiments.yaml`) with missingness regimes (MCAR, block-missing)
- Baseline models (logistic, random forest, simple NN) — to be filled in the `src/pipeline/` modules
- Unit tests and CI (GitHub Actions)
- Makefile with reproducible environment setup (pip, conda, Docker)

## Quickstart
```bash
make env         # create/update conda env (auto-generates environment.yml)
make run         # run baseline pipeline
# or via Docker
make docker-build-train && make docker-run-train
```

Example request:
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json"   -d '{"features":{"g1":1.0,"g2":-2.0,"g3":0.5},"masks":{"g1":1,"g2":1,"g3":0}}'
```

## Environment Setup

### Option A: Pip / Colab (lightweight)
```bash
pip install -r requirements.txt
python scripts/train.py --config configs/experiments.yaml
```

### Option B: Conda + Makefile (recommended)
```bash
make env          # create/update env (pip inside conda)
make env-update   # update from environment.yml
make run          # run baseline
make freeze       # export pinned deps to requirements-lock.txt
make clean        # remove caches
```

Optional Conda extras (CUDA, MKL):
```bash
make env-conda CONDA_DEPS="pytorch pytorch-cuda=12.1" CONDA_CHANNELS="pytorch nvidia conda-forge"
```

Pure Conda convenience (no YAML/pip):
```bash
make conda-env
```

### Option C: Docker (full reproducibility)
```bash
make docker-build-train
make docker-run-train
# after adding FastAPI app/main.py:
make docker-build-api
make docker-run-api
```

## Download & Ingest Data

1. Download TCGA data:
   ```bash
   make data-tcga
   ```
   Downloads into:
   - `data/raw/tcga/tcga_RSEM_gene_tpm.gz`
   - `data/raw/supplemental/Survival_SupplementalTable_S1_20171025_xena_sp`

2. Ingest and preprocess:
   ```bash
   make data-real
   ```
   Extracts `.tsv`, skips duplicate copies, and organizes:
   ```
   data/raw/
     ├── tcga/
     │   ├── tcga_RSEM_gene_tpm.gz
     │   └── tcga_RSEM_gene_tpm.tsv
     └── supplemental/
         └── Survival_SupplementalTable_S1_20171025_xena_sp
   ```

3. Full reset (clean and reload end-to-end):
   ```bash
   make data-reset

## Roadmap (execution order)
1. **Phase 1:** Baselines under complete vs missing data (MCAR, block-missing). Metrics: AUROC/AUPRC.
2. **Phase 2:** Simple robustness methods: mean/zero + mask, matrix completion (softImpute), cross-modal ridge (RNA→pseudo-proteome).
3. **Phase 3:** Productionization: clean configs, reproducible runs, API/dashboard.
4. **Phase 4:** Critical analysis vs frontier methods (GNNs, Transformers, CODE-AE, diffusion) — *discussion only* in the public version.

## Discussion pointers (for the blog post)
- Missing-modality robustness is often **under-reported**. Publish curves of performance vs % missing.
- Advanced architectures add value only if they **respect masks** / domain shift; otherwise they overfit.

## Contributing / Extending
- Drop in alternative models in `src/pipeline/`
- Add new missingness regimes in `configs/experiments.yaml`
- PRs for better baselines welcome
