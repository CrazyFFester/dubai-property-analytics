# Dubai Property Analytics

Pipeline and analysis of Dubai real estate transactions from DLD Open Data:
CSV export → validated `Transaction` records → PostgreSQL, then EDA and price modeling.

## Stack
Python 3.13 · uv · PostgreSQL 17 (Docker Compose) · psycopg 3 · pytest · Ruff

## Roadmap
- [x] Project skeleton (uv, src layout, Ruff, pytest)
- [ ] DLD Open Data → PostgreSQL ingestion + tests
  - [x] Row parsing into a typed `Transaction` (decimals, booleans, optional fields)
  - [x] DB connection from environment
  - [ ] Bulk CSV parsing with header check and bad-row logging
  - [ ] Schema + loading into PostgreSQL
- [ ] EDA
- [ ] Price modeling

## Data
Transactions CSV from the [Dubai Land Department Open Data](https://dubailand.gov.ae/en/open-data/real-estate-data/)
portal. Put raw exports into `data/raw/` (gitignored).

Parsing conventions:
- money as `Decimal` in AED, areas in square meters (`_sqm` suffix)
- empty or whitespace-only optional fields become `None`
- invalid values raise `ValueError`

## Layout
```
src/dubai_property_analytics/
  parsing.py   Transaction dataclass, parse_row and _parse_* helpers
  db.py        connection params from env, connect()
tests/         one test module per source module
data/raw/      raw DLD exports (gitignored)
```

## Setup
```sh
cp .env.example .env                           # set POSTGRES_PASSWORD
docker compose up -d
uv sync
```

## Development
```sh
uv run ruff check --fix && uv run ruff format  # lint + format
uv run pytest -q                               # unit tests
uv run --env-file .env pytest -m integration   # needs running Postgres
```
