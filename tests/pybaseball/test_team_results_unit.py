import pytest
from bs4 import BeautifulSoup

import pybaseball.team_results as tr


def test_schedule_and_record_invalid_team(monkeypatch):
    def fake_get_soup(season, team):
        return BeautifulSoup("<html></html>", "lxml")

    monkeypatch.setattr(tr, "get_soup", fake_get_soup)

    with pytest.raises(ValueError):
        tr.schedule_and_record(2019, "TBR")


def test_schedule_and_record_invalid_season(monkeypatch):
    with pytest.raises(ValueError):
        tr.schedule_and_record(1995, "TBR")
