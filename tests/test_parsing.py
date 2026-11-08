import pytest

from dubai_property_analytics.parsing import _none_if_empty


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("", None),
        ("  ", None),
        ("Samana Lake Views", "Samana Lake Views"),
        (" Marina Mall ", "Marina Mall"),
    ],
)
def test_cleaned_data(raw: str, expected: str) -> None:
    assert _none_if_empty(raw) == expected
