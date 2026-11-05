.DEFAULT_GOAL := help
COMPOSE ?= docker compose

.PHONY: help up down logs build migrate seed lint format typecheck test check clean flows-check staging-up staging-down staging-logs smoke

help: ## Tampilkan daftar perintah
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

up: ## Jalankan stack lokal (db, backend, frontend)
	$(COMPOSE) up -d --build

down: ## Matikan stack lokal
	$(COMPOSE) down

logs: ## Lihat log layanan
	$(COMPOSE) logs -f --tail=100

build: ## Build image backend dan frontend
	$(COMPOSE) build

migrate: ## Terapkan migrasi database (Alembic)
	$(COMPOSE) run --rm backend alembic upgrade head

seed: ## Muat data katalog dari data/seed
	$(COMPOSE) run --rm backend python -m scripts.seed

lint: ## Cek gaya kode (ruff, eslint)
	cd backend && ruff check . && ruff format --check .
	cd frontend && npm run lint

format: ## Rapikan kode
	cd backend && ruff check --fix . && ruff format .
	cd frontend && npm run format

typecheck: ## Cek tipe (mypy, tsc)
	cd backend && mypy app
	cd frontend && npm run typecheck

test: ## Jalankan seluruh test
	cd backend && pytest -q
	cd frontend && npm test

flows-check: ## Validasi flow Langflow yang diekspor (JSON, varian, rahasia)
	python3 langflow/scripts/validate_flows.py

check: lint typecheck test flows-check ## Gerbang kualitas: lint + typecheck + test + flow

clean: ## Hapus container, volume, dan cache
	$(COMPOSE) down -v
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

STAGING = $(COMPOSE) -f docker-compose.yml -f docker-compose.staging.yml

staging-up: ## Jalankan staging lokal (meniru cloud; jalankan dari cabang dev)
	$(STAGING) up -d --build

staging-down: ## Matikan staging lokal
	$(STAGING) down

staging-logs: ## Log staging lokal
	$(STAGING) logs -f --tail=100

smoke: ## Smoke test layanan (lokal atau cloud, lihat scripts/smoke.sh)
	bash scripts/smoke.sh
