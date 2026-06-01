import pytest
from unittest.mock import patch
from datetime import date
from main import find_most_active_cookies, parse_date, load_rows
import sys
import main as main_module

def test_most_active_cookie_single():
    rows = [
        {"cookie": "AtY0laUfhglK3lC7", "timestamp": "2018-12-09T14:19:00+00:00"},
        {"cookie": "SAZuXPGUrfbcn5UA", "timestamp": "2018-12-09T10:13:00+00:00"},
        {"cookie": "5UAVanZf6UtGyKVS", "timestamp": "2018-12-09T07:25:00+00:00"},
        {"cookie": "AtY0laUfhglK3lC7", "timestamp": "2018-12-09T06:19:00+00:00"},
        {"cookie": "SAZuXPGUrfbcn5UA", "timestamp": "2018-12-08T22:03:00+00:00"},
        {"cookie": "4sMM2LxV07bPJzwf", "timestamp": "2018-12-08T21:30:00+00:00"},
        {"cookie": "fbcn5UAVanZf6UtG", "timestamp": "2018-12-08T09:30:00+00:00"},
        {"cookie": "4sMM2LxV07bPJzwf", "timestamp": "2018-12-07T23:30:00+00:00"},
    ]

    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert result == ["AtY0laUfhglK3lC7"]

def test_most_active_cookie_multiple_results():
    rows = [
        {"cookie": "abc", "timestamp": "2018-12-09T10:00:00+00:00"},
        {"cookie": "abc", "timestamp": "2018-12-09T11:00:00+00:00"},
        {"cookie": "xyz", "timestamp": "2018-12-09T12:00:00+00:00"},
        {"cookie": "xyz", "timestamp": "2018-12-09T13:00:00+00:00"},
    ]

    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert set(result) == {"abc", "xyz"}

def test_no_results_for_date_returns_empty():
    rows = [
        {"cookie": "abc", "timestamp": "2018-12-09T10:00:00+00:00"},
    ]

    result = find_most_active_cookies(rows, date(2018, 12, 10))
    assert result == []

def test_empty_input_returns_empty():

    result = find_most_active_cookies([], date(2018, 12, 9))
    assert result == []


def test_timezone_offset_shifts_to_previous_day():
    rows = [
        {"cookie": "abc", "timestamp": "2018-12-09T02:00:00+05:00"},
    ]

    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert result == []

def test_main_end_to_end(tmp_path, capsys, monkeypatch):
    log = tmp_path / "temp_log.csv"
    log.write_text(
        "cookie,timestamp\n"
        "AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
        "AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00\n"
        "SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "argv", ["most-active-cookie", "-f", str(log), "-d", "2018-12-09"])
    main_module.main()

    out = capsys.readouterr().out
    assert out.strip() == "AtY0laUfhglK3lC7"

#error handling
#parse_data

def test_invalid_date_format(caplog):
    with pytest.raises(SystemExit) as exc_info:
        parse_date("2018/12/09")
    assert exc_info.value.code == 1

    assert "2018/12/09" in caplog.text

def test_invalid_date_nonsense_exits(capsys):
    with pytest.raises(SystemExit) as exc_info:
        parse_date("not-a-date")
    assert exc_info.value.code == 1

#load_rows

def test_file_not_found_exits(caplog):
    with pytest.raises(SystemExit) as exc_info:
        load_rows("/nonexistent/path/cookie_log.csv")
    assert exc_info.value.code == 1

    assert "not found" in caplog.text.lower()

def test_directory_passed_instead_of_file_exits(tmp_path, capsys):
    with pytest.raises(SystemExit) as exc_info:
        load_rows(str(tmp_path))
    assert exc_info.value.code == 1

def test_permission_error_exits(caplog):
    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(SystemExit) as exc_info:
            load_rows("random_path.csv")
    assert exc_info.value.code == 1

    assert "permission" in caplog.text.lower()

#find_most_active_cookies

def test_invalid_timestamp_skipped(caplog):
    rows = [
        {"cookie": "abc", "timestamp": "not-a-date"},
        {"cookie": "xyz", "timestamp": "2018-12-09T10:00:00+00:00"},
    ]
    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert result == ["xyz"]

    assert "skipping invalid row" in caplog.text.lower()

def test_missing_timestamp_column_skipped(caplog):
    rows = [
        {"cookie": "abc"},
        {"cookie": "xyz", "timestamp": "2018-12-09T10:00:00+00:00"},
    ]
    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert result == ["xyz"]
    assert "skipping invalid row" in caplog.text.lower()

def test_all_rows_invalid_returns_empty(capsys):
    rows = [
        {"cookie": "abc", "timestamp": "bad"},
        {"cookie": "xyz", "timestamp": "bad-but-again"},
        {"cookie": "123", "timestamp": "2016-06-nahh-just-kidding"},
    ]
    result = find_most_active_cookies(rows, date(2018, 12, 9))
    assert result == []
