# A Reproducible Baseline for Multi‑Omics Drug‑Response Prediction

**Goal.** Provide a clean, end‑to‑end baseline pipeline and API scaffold for predicting drug response from multi‑omics data, with explicit stress‑tests for **missing modalities**.

## Why this repo
- Most “SOTA” papers are hard to reproduce. This is a **usable starting point** others can extend.
- Focus on **robustness**: how badly do models degrade as modalities go missing, and which simple strategies help?

## What’s included
- Minimal FastAPI service (`/predict`) and Dockerfile
- Experiment matrix (`configs/experiments.yaml`) with missingness regimes (MCAR, block‑missing)
- Baseline models (logistic, random forest, simple NN) — to be filled in the `src/pipeline/` modules
- Unit tests and CI (GitHub Actions)

## Quickstart
```bash
make setup
make api  # runs on http://localhost:8000
# or via Docker
make docker-build && make docker-run
```

Example request:
```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json"   -d '{"features":{"g1":1.0,"g2":-2.0,"g3":0.5},"masks":{"g1":1,"g2":1,"g3":0}}'
```

## Roadmap (execution order)
1. **Phase 1:** Baselines under complete vs missing data (MCAR, block‑missing). Metrics: AUROC/AUPRC.
2. **Phase 2:** Simple robustness methods: mean/zero + mask, matrix completion (softImpute), cross‑modal ridge (RNA→pseudo‑proteome).
3. **Phase 3:** Productionization: clean configs, reproducible runs, API/dashboard.
4. **Phase 4:** Critical analysis vs frontier methods (GNNs, Transformers, CODE‑AE, diffusion) — *discussion only* in the public version.

## Discussion pointers (for the blog post)
- Missing‑modality robustness is often **under‑reported**. Publish curves of performance vs % missing.
- Advanced architectures add value only if they **respect masks** / domain shift; otherwise they overfit.

## Contributing / Extending
- Drop in alternative models in `src/pipeline/`
- Add new missingness regimes in `configs/experiments.yaml`
- PRs for better baselines welcome
