import pytest

from dubai_property_analytics.db import conn_params, connect


def test_conn_params_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_DB", "d")
    monkeypatch.delenv("POSTGRES_HOST", raising=False)

    params: dict[str, str] = conn_params()

    assert params["host"] == "localhost"
    assert params["dbname"] == "d"


@pytest.mark.integration
def test_select_one() -> None:
    with connect() as conn:
        assert conn.execute("SELECT 1").fetchone() == (1,)
