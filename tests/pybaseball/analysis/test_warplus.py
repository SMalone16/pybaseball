import pandas as pd
from pybaseball.analysis.warplus import position_warplus, shortstop_warplus


def test_shortstop_warplus(monkeypatch):
    batting_df = pd.DataFrame({
        'mlbID': [1, 2],
        'Pos Summary': ['SS', '2B'],
    })
    war_df = pd.DataFrame({
        'mlb_ID': [1, 1, 2],
        'date_ID': ['2021-07-01', '2021-07-02', '2021-07-02'],
        'pos': ['ss', 'ss', '2b'],
        'WAR': [0.1, 0.2, 0.05],
    })

    def batting_mock(start_dt, end_dt):
        return batting_df

    def war_mock(return_all=False):
        assert return_all
        return war_df

    monkeypatch.setattr('pybaseball.analysis.warplus.batting_stats_range', batting_mock)
    monkeypatch.setattr('pybaseball.analysis.warplus.bwar_bat', war_mock)

    result = shortstop_warplus('2021-07-01', '2021-07-02')

    assert not result.empty
    assert 'WAR_plus' in result.columns
    assert result.loc[0, 'WAR_plus'] == 100.0


def test_position_warplus_select_position(monkeypatch):
    batting_df = pd.DataFrame({
        'mlbID': [1, 2],
        'Pos Summary': ['SS', '2B'],
    })
    war_df = pd.DataFrame({
        'mlb_ID': [1, 1, 2],
        'date_ID': ['2021-07-01', '2021-07-02', '2021-07-02'],
        'pos': ['ss', 'ss', '2b'],
        'WAR': [0.1, 0.2, 0.05],
    })

    def batting_mock(start_dt, end_dt):
        return batting_df

    def war_mock(return_all=False):
        return war_df

    monkeypatch.setattr('pybaseball.analysis.warplus.batting_stats_range', batting_mock)
    monkeypatch.setattr('pybaseball.analysis.warplus.bwar_bat', war_mock)

    result = position_warplus('ss', '2021-07-01', '2021-07-02')

    assert not result.empty
    assert 'WAR_plus' in result.columns
    assert result.loc[0, 'WAR_plus'] == 100.0

