from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    transaction_number: str
    date: datetime
    procedure: str
    is_offplan: bool
    is_freehold: bool
    usage: str
    area: str
    property_type: str
    property_subtype: str | None
    value_aed: Decimal
    actual_area_sqm: Decimal | None
    rooms: str | None
    project: str | None
    master_project: str | None


def _none_if_empty(s: str) -> str | None:
    cleaned: str = s.strip()
    if not cleaned:
        return None
    return cleaned
