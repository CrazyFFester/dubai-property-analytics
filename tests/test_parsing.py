import re
from decimal import Decimal

import pytest

from dubai_property_analytics.parsing import (
    _none_if_empty,
    _parse_bool,
    _parse_decimal,
    _parse_optional_decimal,
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


class TestParseOptionalDecimal:
    @pytest.mark.parametrize(("raw", "expected"), [("", None), ("20", Decimal("20")), (" ", None)])
    def test_valid(self, raw: str, expected: Decimal | None) -> None:
        assert _parse_optional_decimal(raw) == expected

    @pytest.mark.parametrize(
        ("raw", "match"),
        [("NaN", "Not a finite decimal"), ("abc", "Not a decimal")],
    )
    def test_invalid(self, raw: str, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            _parse_optional_decimal(raw)
