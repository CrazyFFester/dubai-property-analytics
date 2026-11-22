from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum, unique
from functools import partial


@unique
class Column(StrEnum):
    TRANSACTION_NUMBER = "TRANSACTION_NUMBER"
    INSTANCE_DATE = "INSTANCE_DATE"
    PROCEDURE_EN = "PROCEDURE_EN"
    IS_OFFPLAN_EN = "IS_OFFPLAN_EN"
    IS_FREE_HOLD_EN = "IS_FREE_HOLD_EN"
    USAGE_EN = "USAGE_EN"
    AREA_EN = "AREA_EN"
    PROP_TYPE_EN = "PROP_TYPE_EN"
    PROP_SB_TYPE_EN = "PROP_SB_TYPE_EN"
    TRANS_VALUE = "TRANS_VALUE"
    ACTUAL_AREA = "ACTUAL_AREA"
    ROOMS_EN = "ROOMS_EN"
    PROJECT_EN = "PROJECT_EN"
    MASTER_PROJECT_EN = "MASTER_PROJECT_EN"


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


def check_header(fieldnames: Collection[str] | None) -> None:
    missing = set(Column) - set(fieldnames or ())
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}")


def parse_row(row: Mapping[str, str | None]) -> Transaction:
    return Transaction(
        transaction_number=_field(row, Column.TRANSACTION_NUMBER, _require_str),
        instance_date=_field(row, Column.INSTANCE_DATE, _parse_datetime),
        procedure=_field(row, Column.PROCEDURE_EN, _require_str),
        is_offplan=_field(row, Column.IS_OFFPLAN_EN, _parse_offplan),
        is_freehold=_field(row, Column.IS_FREE_HOLD_EN, _parse_freehold),
        usage=_field(row, Column.USAGE_EN, _require_str),
        area_name=_field(row, Column.AREA_EN, _require_str),
        property_type=_field(row, Column.PROP_TYPE_EN, _require_str),
        property_subtype=_field(row, Column.PROP_SB_TYPE_EN, _none_if_empty),
        value_aed=_field(row, Column.TRANS_VALUE, _parse_positive_decimal),
        actual_area_sqm=_field(row, Column.ACTUAL_AREA, _parse_positive_decimal),
        rooms=_field(row, Column.ROOMS_EN, _none_if_empty),
        project=_field(row, Column.PROJECT_EN, _none_if_empty),
        master_project=_field(row, Column.MASTER_PROJECT_EN, _none_if_empty),
    )


# Field parsers
def _field[T](row: Mapping[str, str | None], col: Column, parse: Callable[[str], T]) -> T:
    raw = row.get(col)
    if raw is None:
        raise ValueError(f"{col}: missing cell")
    try:
        return parse(raw)
    except ValueError as e:
        raise ValueError(f"{col}: {e}") from e


def _require_str(raw: str) -> str:
    cleaned = raw.strip()
    if not cleaned:
        raise ValueError("empty")
    return cleaned


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


def _parse_positive_decimal(raw: str) -> Decimal:
    number = _parse_decimal(raw)
    if number <= 0:
        raise ValueError(f"must be > 0, got {raw!r}")
    return number


def _parse_datetime(raw: str) -> datetime:
    return datetime.fromisoformat(raw.strip())


def _parse_bool(raw: str, *, true: str, false: str) -> bool:
    cleaned: str = raw.strip()

    if cleaned == true:
        return True
    if cleaned == false:
        return False
    raise ValueError(f"expected {true!r} or {false!r}, got {raw!r}")


_parse_offplan = partial(_parse_bool, true="Off-Plan", false="Ready")
_parse_freehold = partial(_parse_bool, true="Free Hold", false="Non Free Hold")
