from datetime import timedelta
from typing import Optional
import pandas as pd

from ..league_batting_stats import batting_stats_range, bwar_bat
from ..utils import sanitize_date_range
from ..enums.fangraphs import FangraphsPositions


def shortstop_warplus(start_dt: Optional[str] = None, end_dt: Optional[str] = None) -> pd.DataFrame:
    """Calculate WAR+ for shortstops over a given date range.

    If no dates are supplied, the range defaults to the last seven days.
    WAR+ is defined as a player's WAR over the period divided by the average WAR
    for all shortstops in that period, multiplied by 100.
    """
    start_date, end_date = sanitize_date_range(start_dt, end_dt)
    if start_dt is None and end_dt is None:
        start_date = end_date - timedelta(days=6)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    batting = batting_stats_range(start_str, end_str)
    pos_cols = [c for c in batting.columns if "Pos" in c]
    if pos_cols:
        pos_col = pos_cols[0]
        batting = batting[batting[pos_col].str.contains("SS", case=False, na=False)]

    war_data = bwar_bat(return_all=True)
    if "date_ID" in war_data.columns:
        war_data["date_ID"] = pd.to_datetime(war_data["date_ID"])
        mask = (war_data["date_ID"] >= start_date) & (war_data["date_ID"] <= end_date)
    else:
        mask = pd.Series(False, index=war_data.index)

    position_mask = war_data.get("pos", "") == FangraphsPositions.SHORT_STOP.value
    war_period = war_data.loc[mask & position_mask]
    war_by_player = war_period.groupby("mlb_ID")["WAR"].sum()

    avg_war = war_by_player.mean() if not war_by_player.empty else 0
    war_plus = (war_by_player / avg_war * 100).rename("WAR_plus") if avg_war else war_by_player * 0

    result = pd.concat([war_by_player.rename("WAR"), war_plus], axis=1).reset_index()
    return result

