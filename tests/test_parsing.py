from decimal import Decimal

import pytest

from dubai_property_analytics.parsing import (
    _bool_from,
    _decimal,
    _decimal_or_none,
    _none_if_empty,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("", None),
        ("  ", None),
        ("Samana Lake Views", "Samana Lake Views"),
        (" Marina Mall ", "Marina Mall"),
    ],
)
def test_none_if_empty(raw: str, expected: str | None) -> None:
    assert _none_if_empty(raw) == expected


@pytest.mark.parametrize(
    "value, true, false, expected",
    [
        ("Off-Plan", "Off-Plan", "Ready", True),
        (" Off-Plan ", "Off-Plan", "Ready", True),
        ("Ready", "Off-Plan", "Ready", False),
        ("Free Hold", "Free Hold", "Non Free Hold", True),
        ("Non Free Hold", "Free Hold", "Non Free Hold", False),
    ],
)
def test_bool_from_valid(value: str, true: str, false: str, expected: bool) -> None:
    assert _bool_from(value, true=true, false=false) == expected


@pytest.mark.parametrize(
    "value, true, false",
    [
        ("", "Off-Plan", "Ready"),
        ("Off-plan", "Off-Plan", "Ready"),
        ("Off-Plane", "Off-Plan", "Ready"),
        ("Free Hold", "Off-Plan", "Ready"),
    ],
)
def test_bool_from_invalid(value: str, true: str, false: str) -> None:
    with pytest.raises(ValueError):
        _bool_from(value, true=true, false=false)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("20", Decimal("20")),
        ("20.5", Decimal("20.5")),
        ("-20", Decimal("-20")),
        (" 20 ", Decimal("20")),
    ],
)
def test_decimal_valid(value: str, expected: Decimal) -> None:
    assert _decimal(value) == expected


@pytest.mark.parametrize("value", ["abc", "", "1,5", "NaN", "Infinity", "-inf", "sNaN"])
def test_decimal_invalid(value: str) -> None:
    with pytest.raises(ValueError):
        _decimal(value)


@pytest.mark.parametrize("value, expected", [("", None), ("20", Decimal("20")), (" ", None)])
def test_decimal_or_none_valid(value: str, expected: Decimal | None) -> None:
    assert _decimal_or_none(value) == expected


@pytest.mark.parametrize(
    "value, match", [("NaN", "Not a finite decimal"), ("abc", "Not a decimal")]
)
def test_decimal_or_none_invalid(value: str, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        _decimal_or_none(value)
