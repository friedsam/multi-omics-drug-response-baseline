# ---- config ----
ENV_NAME ?= multiomics
PY       := conda run -n $(ENV_NAME) python
PIP      := conda run -n $(ENV_NAME) pip

# Optional: extra Conda packages/channels (for MKL, CUDA, etc.)
# Example use:
#   make env-conda CONDA_DEPS="pytorch pytorch-cuda=12.1" CONDA_CHANNELS="pytorch nvidia conda-forge"
CONDA_DEPS     ?=
CONDA_CHANNELS ?= conda-forge

# ---- public targets ----
.PHONY: help env env-update env-conda env-conda-update run freeze clean

help:
	@echo "make env             # auto-gen environment.yml from requirements.txt + create/update env"
	@echo "make env-update      # update existing env from environment.yml"
	@echo "make env-conda       # (optional) include Conda-only deps via CONDA_DEPS/CONDA_CHANNELS"
	@echo "make env-conda-update# update existing env with Conda-only deps"
	@echo "make run             # run baseline pipeline"
	@echo "make freeze          # write pip freeze to requirements-lock.txt"
	@echo "make clean           # remove caches"

# ---- default: generate environment.yml from requirements.txt (pip-first) ----
environment.yml: requirements.txt
	@echo "name: $(ENV_NAME)"                >  $@
	@echo "channels:"                       >> $@
	@echo "  - conda-forge"                 >> $@
	@echo "dependencies:"                   >> $@
	@echo "  - python=3.10"                 >> $@
	@echo "  - pip"                         >> $@
	@echo "  - pip:"                        >> $@
	@echo "      - -r requirements.txt"     >> $@
	@echo "[ok] regenerated $@ from requirements.txt"

env: environment.yml
	@command -v conda >/dev/null 2>&1 || { echo >&2 "Conda not found."; exit 1; }
	@if conda env list | grep -qE "^$(ENV_NAME)\s"; then \
		echo "[update] $(ENV_NAME)"; \
		conda env update -n $(ENV_NAME) -f environment.yml --prune; \
	else \
		echo "[create] $(ENV_NAME)"; \
		conda env create -n $(ENV_NAME) -f environment.yml; \
	fi
	@echo "[ok] conda env ready: $(ENV_NAME)"

env-update:
	@conda env update -n $(ENV_NAME) -f environment.yml --prune

# ---- optional: generate YAML including Conda-only deps/channels ----
yaml-conda:
	@echo "name: $(ENV_NAME)"                >  environment.yml
	@echo "channels:"                       >> environment.yml
	@for ch in $(CONDA_CHANNELS); do echo "  - $$ch" >> environment.yml; done
	@echo "dependencies:"                   >> environment.yml
	@echo "  - python=3.10"                 >> environment.yml
	@for pkg in $(CONDA_DEPS); do echo "  - $$pkg" >> environment.yml; done
	@echo "  - pip"                         >> environment.yml
	@echo "  - pip:"                        >> environment.yml
	@echo "      - -r requirements.txt"     >> environment.yml
	@echo "[ok] regenerated environment.yml with Conda deps: $(CONDA_DEPS)"

env-conda: yaml-conda
	@command -v conda >/dev/null 2>&1 || { echo >&2 "Conda not found."; exit 1; }
	@if conda env list | grep -qE "^$(ENV_NAME)\s"; then \
		echo "[update] $(ENV_NAME)"; \
		conda env update -n $(ENV_NAME) -f environment.yml --prune; \
	else \
		echo "[create] $(ENV_NAME)"; \
		conda env create -n $(ENV_NAME) -f environment.yml; \
	fi
	@echo "[ok] conda env ready (conda deps): $(ENV_NAME)"

env-conda-update: yaml-conda
	@conda env update -n $(ENV_NAME) -f environment.yml --prune

# ---- extra: pure conda shortcut (no requirements.txt, no YAML) ----
.PHONY: conda-env
conda-env:
	@echo "[create] $(ENV_NAME) with conda only"
	conda create -y -n $(ENV_NAME) python=3.10 \
	    numpy pandas scipy scikit-learn matplotlib \
	    xgboost lightgbm \
	    pytorch cpuonly -c pytorch -c conda-forge
	@echo "[ok] conda-only env ready: $(ENV_NAME)"

.PHONY: docker-build-train docker-run-train docker-build-api docker-run-api

docker-build-train:
	docker build --target train -t multiomics:train .

docker-run-train:
	docker run --rm -it -v $(PWD)/data:/app/data multiomics:train

docker-build-api:
	docker build --target api -t multiomics:api .

docker-run-api:
	docker run --rm -p 8000:8000 multiomics:api

# ---- run / utilities ----
run:
	$(PY) scripts/train.py --config configs/experiments.yaml

freeze:
	$(PIP) freeze | sed '/^@/d' > requirements-lock.txt
	@echo "[ok] wrote requirements-lock.txt"

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
