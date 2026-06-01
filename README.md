# most_active_cookie

## About

A command-line tool that finds the most active cookie(s) from an activity log file for a given date.

### Assumptions

- Cookies in the log file are sorted by timestamp, from newest to oldest calls.
- If more than one cookie is the most active, all of them are returned.
- Dates are taken in UTC timezone.

## Built With

- Python 3.9+ (standard library only: `csv`, `argparse`, `datetime`, `collections`, `logging`)
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

### Install as a command (optional)

Installing the project provides a `most-active-cookie` command. I recommended a virtual environment.

```sh
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux
pip install .
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

### Installed Command (`most-active-cookie`)

If you installed the project ([Install as a command](#install-as-a-command-optional)), run it directly:

```sh
most-active-cookie -f cookie_log.csv -d 2018-12-09
```

This is the same as the `python main.py` command above.

### Tests (`test_main.py`)

To run all test files:

```sh
pytest -v
```
