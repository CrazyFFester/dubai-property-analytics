import re
from datetime import datetime
from decimal import Decimal

import pytest

from dubai_property_analytics.parsing import (
    Column,
    Transaction,
    _none_if_empty,
    _parse_bool,
    _parse_decimal,
    parse_row,
)


class TestNoneIfEmpty:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("", None),
            ("  ", None),
            ("Samana Lake Views", "Samana Lake Views"),
            (" Marina Mall ", "Marina Mall"),
        ],
    )
    def test_cases(self, raw: str, expected: str | None) -> None:
        assert _none_if_empty(raw) == expected


class TestParseBool:
    @pytest.mark.parametrize(
        ("raw", "true", "false", "expected"),
        [
            ("Off-Plan", "Off-Plan", "Ready", True),
            (" Off-Plan ", "Off-Plan", "Ready", True),
            ("Ready", "Off-Plan", "Ready", False),
            ("Free Hold", "Free Hold", "Non Free Hold", True),
            ("Non Free Hold", "Free Hold", "Non Free Hold", False),
        ],
    )
    def test_valid(self, raw: str, true: str, false: str, expected: bool) -> None:
        assert _parse_bool(raw, true=true, false=false) == expected

    @pytest.mark.parametrize(
        ("raw", "true", "false"),
        [
            ("", "Off-Plan", "Ready"),
            ("Off-plan", "Off-Plan", "Ready"),
            ("Off-Plane", "Off-Plan", "Ready"),
            ("Free Hold", "Off-Plan", "Ready"),
        ],
    )
    def test_invalid(self, raw: str, true: str, false: str) -> None:
        with pytest.raises(
            ValueError, match=re.escape(f"expected {true!r} or {false!r}, got {raw!r}")
        ):
            _parse_bool(raw, true=true, false=false)


class TestParseDecimal:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("20", Decimal("20")),
            ("20.5", Decimal("20.5")),
            ("-20", Decimal("-20")),
            (" 20 ", Decimal("20")),
        ],
    )
    def test_valid(self, raw: str, expected: Decimal) -> None:
        assert _parse_decimal(raw) == expected

    @pytest.mark.parametrize(
        ("raw", "match"),
        [
            ("abc", "Not a decimal"),
            ("", "Not a decimal"),
            ("1,5", "Not a decimal"),
            ("NaN", "Not a finite decimal"),
            ("Infinity", "Not a finite decimal"),
            ("-inf", "Not a finite decimal"),
            ("sNaN", "Not a finite decimal"),
        ],
    )
    def test_invalid(self, raw: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            _parse_decimal(raw)


@pytest.fixture
def valid_row() -> dict[str, str | None]:
    return {
        Column.TRANSACTION_NUMBER: "1-102-2026-1234",
        Column.INSTANCE_DATE: "2026-10-15 00:00:00",
        Column.PROCEDURE_EN: "Sell",
        Column.IS_OFFPLAN_EN: "Ready",
        Column.IS_FREE_HOLD_EN: "Free Hold",
        Column.USAGE_EN: "Residential",
        Column.AREA_EN: " Marsa Dubai ",
        Column.PROP_TYPE_EN: "Unit",
        Column.PROP_SB_TYPE_EN: "Flat",
        Column.TRANS_VALUE: "1500000",
        Column.ACTUAL_AREA: "85.5",
        Column.ROOMS_EN: "1 B/R",
        Column.PROJECT_EN: "Marina Gate",
        Column.MASTER_PROJECT_EN: "",
    }


class TestParseRow:
    def test_valid(self, valid_row: dict[str, str | None]) -> None:
        assert parse_row(valid_row) == Transaction(
            transaction_number="1-102-2026-1234",
            instance_date=datetime(2026, 10, 15),
            procedure="Sell",
            is_offplan=False,
            is_freehold=True,
            usage="Residential",
            area_name="Marsa Dubai",
            property_type="Unit",
            property_subtype="Flat",
            value_aed=Decimal("1500000"),
            actual_area_sqm=Decimal("85.5"),
            rooms="1 B/R",
            project="Marina Gate",
            master_project=None,
        )

    @pytest.mark.parametrize(
        ("col", "attr"),
        [
            (Column.PROP_SB_TYPE_EN, "property_subtype"),
            (Column.ROOMS_EN, "rooms"),
            (Column.PROJECT_EN, "project"),
            (Column.MASTER_PROJECT_EN, "master_project"),
        ],
    )
    def test_optional_empty_is_none(
        self, valid_row: dict[str, str | None], col: Column, attr: str
    ) -> None:
        assert getattr(parse_row(valid_row | {col: " "}), attr) is None

    @pytest.mark.parametrize(
        "col",
        [
            Column.TRANSACTION_NUMBER,
            Column.PROCEDURE_EN,
            Column.USAGE_EN,
            Column.AREA_EN,
            Column.PROP_TYPE_EN,
        ],
    )
    @pytest.mark.parametrize("raw", ["", " "])
    def test_required_empty(self, valid_row: dict[str, str | None], col: Column, raw: str) -> None:
        with pytest.raises(ValueError, match=f"^{re.escape(f'{col}: empty')}$") as exc:
            parse_row(valid_row | {col: raw})
        assert isinstance(exc.value.__cause__, ValueError)

    @pytest.mark.parametrize("col", [Column.TRANS_VALUE, Column.ACTUAL_AREA])
    @pytest.mark.parametrize("raw", ["0", "0.00", "-1"])
    def test_non_positive(self, valid_row: dict[str, str | None], col: Column, raw: str) -> None:
        with pytest.raises(ValueError, match=f"^{col}: must be > 0"):
            parse_row(valid_row | {col: raw})

    @pytest.mark.parametrize("col", list(Column))
    def test_missing_cell(self, valid_row: dict[str, str | None], col: Column) -> None:
        with pytest.raises(ValueError, match=f"^{col}: missing cell$"):
            parse_row(valid_row | {col: None})

    def test_invalid_datetime(self, valid_row: dict[str, str | None]) -> None:
        with pytest.raises(ValueError, match=f"^{Column.INSTANCE_DATE}: "):
            parse_row(valid_row | {Column.INSTANCE_DATE: "15/10/2026"})

    def test_invalid_bool(self, valid_row: dict[str, str | None]) -> None:
        with pytest.raises(ValueError, match=f"^{Column.IS_OFFPLAN_EN}: expected"):
            parse_row(valid_row | {Column.IS_OFFPLAN_EN: "Off-plan"})
