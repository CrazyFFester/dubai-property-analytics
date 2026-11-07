from dubai_property_analytics import main


def test_main_runs(capsys) -> None:
    main()
    assert "dubai-property-analytics" in capsys.readouterr().out
