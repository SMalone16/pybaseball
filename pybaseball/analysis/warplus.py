from datetime import timedelta
from typing import Optional

import pandas as pd

from ..league_batting_stats import batting_stats_range, bwar_bat
from ..league_pitching_stats import pitching_stats_range, bwar_pitch

from ..utils import sanitize_date_range
from ..enums.fangraphs import FangraphsPositions



def position_warplus(
    position: Optional[str] = FangraphsPositions.ALL.value,
    start_dt: Optional[str] = None,
    end_dt: Optional[str] = None,
    stat_type: str = "bat",
) -> pd.DataFrame:
    """Calculate WAR+ for the specified position over a given date range.

    Parameters
    ----------
    position : str or None, default ``FangraphsPositions.ALL``
        Fangraphs position code to filter on. ``None`` or ``'all'`` will return
        results for all players.
    start_dt, end_dt : str, optional
        Date range in ``YYYY-MM-DD`` format. If both are ``None`` the last seven
        days are used.
    stat_type : {'bat', 'pitch'}, default 'bat'
        Whether to use batting or pitching statistics and WAR tables.
    """

    start_date, end_date = sanitize_date_range(start_dt, end_dt)
    if start_dt is None and end_dt is None:
        start_date = end_date - timedelta(days=6)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")


    if stat_type == "bat":
        stats_df = batting_stats_range(start_str, end_str)
        war_data = bwar_bat(return_all=True)
    elif stat_type == "pitch":
        stats_df = pitching_stats_range(start_str, end_str)
        war_data = bwar_pitch(return_all=True)
    else:
        raise ValueError("stat_type must be 'bat' or 'pitch'")

    if position and position != FangraphsPositions.ALL.value:
        pos_cols = [c for c in stats_df.columns if "Pos" in c]
        if pos_cols:
            pos_col = pos_cols[0]

            stats_df = stats_df[
                stats_df[pos_col].str.contains(position, case=False, na=False)
            ]

        position_mask = war_data.get("pos", "") == position
    else:
        position_mask = pd.Series(True, index=war_data.index)

    if "date_ID" in war_data.columns:
        war_data["date_ID"] = pd.to_datetime(war_data["date_ID"])
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        mask = (war_data["date_ID"] >= start_ts) & (war_data["date_ID"] <= end_ts)
    else:
        mask = pd.Series(False, index=war_data.index)

    war_period = war_data.loc[mask & position_mask]
    war_by_player = war_period.groupby("mlb_ID")["WAR"].sum()

    avg_war = war_by_player.mean() if not war_by_player.empty else 0

    war_plus = (
        (war_by_player / avg_war * 100).rename("WAR_plus")
        if avg_war
        else war_by_player * 0
    )


    result = pd.concat([war_by_player.rename("WAR"), war_plus], axis=1).reset_index()
    return result

def shortstop_warplus(
    start_dt: Optional[str] = None, end_dt: Optional[str] = None
) -> pd.DataFrame:

    """Backward compatible wrapper for shortstop WAR+."""
    return position_warplus(
        position=FangraphsPositions.SHORT_STOP.value,
        start_dt=start_dt,
        end_dt=end_dt,
        stat_type="bat",
    )
