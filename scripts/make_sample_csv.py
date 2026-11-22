"""Build tests/fixtures/sample.csv from a raw DLD export."""

import csv
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path


src = Path(sys.argv[1])
dst = Path("tests/fixtures/sample.csv")

with src.open(encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)
assert fieldnames is not None

counts = Counter(r["TRANSACTION_NUMBER"] for r in rows)
dup = next(k for k, c in counts.items() if c > 1)
dup_rows = [r for r in rows if r["TRANSACTION_NUMBER"] == dup]
singles = [r for r in rows if counts[r["TRANSACTION_NUMBER"]] == 1]
with_master = next(r for r in singles if r["MASTER_PROJECT_EN"].strip())
normal = [r for r in singles if r is not with_master][:5]
conflict = normal[0] | {"TRANS_VALUE": str(Decimal(normal[0]["TRANS_VALUE"]) + 1)}

out = [*normal, with_master, *dup_rows, conflict]
dst.parent.mkdir(parents=True, exist_ok=True)
with dst.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(out)

print(f"{dst}: {len(out)} rows; dup={dup}; conflict={normal[0]['TRANSACTION_NUMBER']}")
