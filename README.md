# most_active_cookie

## About

A command-line tool that finds the most active cookie(s) from an activity log file for a given date.

### Assumptions

- Cookies in the log file are sorted by timestamp, from newest to oldest calls.
- If more than one cookie is the most active, all of them are returned.
- Dates are taken in UTC timezone.

## Built With

- Python 3.9+ (standard library only: `csv`, `argparse`, `datetime`, `collections`)
- [pytest](https://pytest.org) for testing

## Getting Started

### Prerequisites

Python 3.9+ required. Install the dependencies (pytest) to run the test cases:

```sh
pip install --group dev
```

> Requires pip 25.1+ (for `[dependency-groups]` support). With [uv](https://docs.astral.sh/uv/), run `uv sync` instead.

### Installation

```sh
git clone https://github.com/ToluOlas/most_active_cookie.git
cd most_active_cookie
```

## Usage

### Main Program (`main.py`)

The proper format for calling the main program in terminal:

```
python main.py -f <log_file> -d <YYYY-MM-DD>
```

| Flag | Description |
|------|-------------|
| `-f` | Path to the CSV log file |
| `-d` | Date to query in `YYYY-MM-DD` format |

**Example** — most active cookie on the 9th of December 2018:

```sh
python main.py -f cookie_log.csv -d 2018-12-09
```

Output:

```
AtY0laUfhglK3lC7
```

### Tests (`test_main.py`)

To run all test files:

```sh
pytest -v
```
