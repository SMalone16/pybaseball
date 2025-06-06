from typing import Callable

import pandas as pd
import requests
from pytest import MonkeyPatch

from pybaseball.top_prospects import top_prospects


def test_top_prospects_returns_dataframe(monkeypatch: MonkeyPatch, get_data_file_contents: Callable[[str], str]) -> None:
    html = get_data_file_contents('top_prospects.html')
    expected_url = 'https://www.mlb.com/prospects/stats?teamId=117'

    def fake_get(url: str, params: None = None, timeout: None = None, headers: None = None):
        assert url == expected_url

        class DummyResponse:
            def __init__(self, content: str):
                self.content = content.encode("utf-8")

            def raise_for_status(self) -> None:  # pragma: no cover - no failure path
                pass

        return DummyResponse(html)

    monkeypatch.setattr(requests, "get", fake_get)

    result = top_prospects("astros")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty


