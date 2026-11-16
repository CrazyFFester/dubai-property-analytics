from decimal import Decimal

import pytest

from dubai_property_analytics.parsing import (
    _bool_from,
    _decimal,
    _decimal_or_none,
    _none_if_empty,
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


class TestBoolFrom:
    @pytest.mark.parametrize(
        ("value", "true", "false", "expected"),
        [
            ("Off-Plan", "Off-Plan", "Ready", True),
            (" Off-Plan ", "Off-Plan", "Ready", True),
            ("Ready", "Off-Plan", "Ready", False),
            ("Free Hold", "Free Hold", "Non Free Hold", True),
            ("Non Free Hold", "Free Hold", "Non Free Hold", False),
        ],
    )
    def test_valid(self, value: str, true: str, false: str, expected: bool) -> None:
        assert _bool_from(value, true=true, false=false) == expected

    @pytest.mark.parametrize(
        ("value", "true", "false"),
        [
            ("", "Off-Plan", "Ready"),
            ("Off-plan", "Off-Plan", "Ready"),
            ("Off-Plane", "Off-Plan", "Ready"),
            ("Free Hold", "Off-Plan", "Ready"),
        ],
    )
    def test_invalid(self, value: str, true: str, false: str) -> None:
        with pytest.raises(ValueError):
            _bool_from(value, true=true, false=false)


class TestDecimal:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("20", Decimal("20")),
            ("20.5", Decimal("20.5")),
            ("-20", Decimal("-20")),
            (" 20 ", Decimal("20")),
        ],
    )
    def test_valid(self, value: str, expected: Decimal) -> None:
        assert _decimal(value) == expected

    @pytest.mark.parametrize(
        ("value", "match"),
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
    def test_invalid(self, value: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            _decimal(value)


class TestDecimalOrNone:
    @pytest.mark.parametrize(
        ("value", "expected"), [("", None), ("20", Decimal("20")), (" ", None)]
    )
    def test_valid(self, value: str, expected: Decimal | None) -> None:
        assert _decimal_or_none(value) == expected

    @pytest.mark.parametrize(
        ("value", "match"),
        [("NaN", "Not a finite decimal"), ("abc", "Not a decimal")],
    )
    def test_invalid(self, value: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            _decimal_or_none(value)
