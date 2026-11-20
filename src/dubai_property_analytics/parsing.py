from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation


@dataclass(frozen=True)
class Transaction:
    transaction_number: str
    instance_date: datetime
    procedure: str
    is_offplan: bool
    is_freehold: bool
    usage: str
    area_name: str
    property_type: str
    property_subtype: str | None
    value_aed: Decimal
    actual_area_sqm: Decimal
    rooms: str | None
    project: str | None
    master_project: str | None


def _none_if_empty(raw: str) -> str | None:
    cleaned: str = raw.strip()
    if not cleaned:
        return None
    return cleaned


def _parse_decimal(raw: str) -> Decimal:
    cleaned: str = raw.strip()

    try:
        number = Decimal(cleaned)
    except InvalidOperation as e:
        raise ValueError(f"Not a decimal {raw!r}") from e

    if not number.is_finite():
        raise ValueError(f"Not a finite decimal {raw!r}")

    return number


def _parse_bool(raw: str, *, true: str, false: str) -> bool:
    cleaned: str = raw.strip()

    if cleaned == true:
        return True
    if cleaned == false:
        return False
    raise ValueError(f"expected {true!r} or {false!r}, got {raw!r}")


def parse_row(row: dict[str, str]) -> Transaction:
    return Transaction(
        transaction_number=row["TRANSACTION_NUMBER"],
        instance_date=datetime.fromisoformat(row["INSTANCE_DATE"]),
        procedure=row["PROCEDURE_EN"],
        is_offplan=_parse_bool(row["IS_OFFPLAN_EN"], true="Off-Plan", false="Ready"),
        is_freehold=_parse_bool(row["IS_FREE_HOLD_EN"], true="Free Hold", false="Non Free Hold"),
        usage=row["USAGE_EN"],
        area_name=row["AREA_EN"],
        property_type=row["PROP_TYPE_EN"],
        property_subtype=_none_if_empty(row["PROP_SB_TYPE_EN"]),
        value_aed=_parse_decimal(row["TRANS_VALUE"]),
        actual_area_sqm=_parse_decimal(row["ACTUAL_AREA"]),
        rooms=_none_if_empty(row["ROOMS_EN"]),
        project=_none_if_empty(row["PROJECT_EN"]),
        master_project=_none_if_empty(row["MASTER_PROJECT_EN"]),
    )
