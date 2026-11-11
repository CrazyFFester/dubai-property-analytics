import pytest

from dubai_property_analytics.parsing import _bool_from, _none_if_empty


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("", None),
        ("  ", None),
        ("Samana Lake Views", "Samana Lake Views"),
        (" Marina Mall ", "Marina Mall"),
    ],
)
def test_cleaned_data(raw: str, expected: str | None) -> None:
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
def test_bool_from_valid(
    value: str, true: str, false: str, expected: bool
) -> None:
    assert _bool_from(value, true=true, false=false) == expected


@pytest.mark.parametrize(
    "value, true, false",
    [
        ("", "Off-Plan", "Ready"),
        ("Off-plan", "Off-Plan", "Ready"),
        ("Off-Plane", "Off-Plan", "Ready"),
        ("Free Hold", "Off-Plan", "Ready"),
        # 4 кейса: пустая строка, другой регистр, мусор, значение из чужой колонки
    ],
)
def test_bool_from_invalid(value: str, true: str, false: str) -> None:
    with pytest.raises(ValueError):
        _bool_from(value, true=true, false=false)
