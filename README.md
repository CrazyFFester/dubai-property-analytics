# Dubai Property Analytics

Pipeline and analysis of Dubai real estate transactions from DLD Open Data.

## Stack
Python 3.13 · uv · PostgreSQL (Docker) · pytest · Ruff

## Roadmap
- [x] Project skeleton (uv, src layout, Ruff, pytest)
- [ ] DLD Open Data → PostgreSQL ingestion + tests
- [ ] EDA
- [ ] Price modeling

## Setup
```bash
cp .env.example .env
docker compose up -d
uv sync
uv run pytest                                  # unit tests
uv run --env-file .env pytest -m integration   # needs Postgres
```
