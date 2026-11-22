# Test fixtures

## sample.csv

Generated from `data/raw/transactions_2026_10.csv`:

    uv run python scripts/make_sample_csv.py data/raw/transactions_2026_10.csv

9 rows, UTF-8 with BOM (as in DLD exports):

- 5 regular rows
- 1 row with non-empty MASTER_PROJECT_EN
- 2 rows `11-33033-2026` — real duplicate, differ only in NEAREST_METRO_EN → equal Transaction, skip
- 1 row `102-54673-2025` — synthetic conflict: copy of a regular row with TRANS_VALUE + 1 → log as conflict
