import pytest
from bs4 import BeautifulSoup
import pandas as pd

import pybaseball.team_results as tr


def test_schedule_and_record_invalid_team(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get_soup(season: int, team: str) -> BeautifulSoup:
        return BeautifulSoup("<html></html>", "lxml")

    monkeypatch.setattr(tr, "get_soup", fake_get_soup)

    with pytest.raises(ValueError):
        tr.schedule_and_record(2019, "TBR")


def test_schedule_and_record_invalid_season(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ValueError):
        tr.schedule_and_record(1995, "TBR")


def test_schedule_and_record_all(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_df = pd.DataFrame({"Tm": ["AAA"], "R": [1], "Attendance": ["0"], "Streak": ["+"]})

    def fake_get_soup(season: int, team: str) -> BeautifulSoup:
        return BeautifulSoup("<html></html>", "lxml")

    def fake_get_table(soup: BeautifulSoup, team: str) -> pd.DataFrame:
        df = fake_df.copy()
        df['Tm'] = team
        return df

    monkeypatch.setattr(tr, "get_soup", fake_get_soup)
    monkeypatch.setattr(tr, "get_table", fake_get_table)
    monkeypatch.setattr(tr, "process_win_streak", lambda df: df)
    monkeypatch.setattr(tr, "make_numeric", lambda df: df)
    monkeypatch.setattr(tr.teamid_lookup, "team_ids", lambda season: pd.DataFrame({'teamIDBR': ['AAA', 'BBB']}))

    result = tr.schedule_and_record(2020)

    assert list(result['Tm']) == ['AAA', 'BBB']

