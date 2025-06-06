import attr
import pandas as pd

@attr.s(auto_attribs=True, slots=True)
class Trajectory:
    """Container for batted ball trajectory data."""

    data: pd.DataFrame

    def to_dataframe(self) -> pd.DataFrame:
        """Return the underlying :class:`pandas.DataFrame`."""
        return self.data

    def __getattr__(self, item):
        return getattr(self.data, item)
