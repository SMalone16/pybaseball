# Record Breaker

`record_breaker` helps identify games where club or league records were set. The module wraps Retrosheet and Baseball Reference data to surface notable performances for any team or span of time.

## Fetching Historical Team Data

```python
from pybaseball import record_breaker

# All record-breaking games in Mets history
mets_history = record_breaker.team_history("NYM")
```

## Analyzing a Single Game

```python
from pybaseball import record_breaker

# Inspect one Mets game by date
single_game = record_breaker.game("2015-07-31", team="NYM")
```

## Scanning a Date Range

```python
from pybaseball import record_breaker

# Find all record breakers early in the 1986 season
records = record_breaker.scan("1986-04-01", "1986-06-30")
```
