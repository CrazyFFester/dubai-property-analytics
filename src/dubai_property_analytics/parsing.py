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


def _decimal_or_none(s: str) -> Decimal | None:
    cleaned: str | None = _none_if_empty(s)
    if cleaned is None:
        return None
    return Decimal(cleaned)


def _bool_from(value: str, *, true: str, false: str) -> bool:
    cleaned = value.strip()

    if cleaned == true:
        return True
    if cleaned == false:
        return False
    raise ValueError(f"expected {true!r} or {false!r}, got {value!r}")


def parse_row(row: dict[str, str]) -> Transaction:
    return Transaction(
        transaction_number=row["TRANSACTION_NUMBER"],
        date=datetime.fromisoformat(row["INSTANCE_DATE"]),
        procedure=row["PROCEDURE_EN"],
        is_offplan=_bool_from(
            row["IS_OFFPLAN_EN"], true="Off-Plan", false="Ready"
        ),
        is_freehold=_bool_from(
            row["IS_FREE_HOLD_EN"], true="Free Hold", false="Non Free Hold"
        ),
        usage=row["USAGE_EN"],
        area=row["AREA_EN"],
        property_type=row["PROP_TYPE_EN"],
        property_subtype=_none_if_empty(row["PROP_SB_TYPE_EN"]),
        value_aed=Decimal(row["TRANS_VALUE"]),
        actual_area_sqm=_decimal_or_none(row["ACTUAL_AREA"]),
        rooms=_none_if_empty(row["ROOMS_EN"]),
        project=_none_if_empty(row["PROJECT_EN"]),
        master_project=_none_if_empty(row["MASTER_PROJECT_EN"]),
    )
