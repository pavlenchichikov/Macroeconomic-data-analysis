import sys
from unittest.mock import mock_open, patch

import pytest

from main import parse_arguments, read_csv_files


@pytest.fixture
def valid_argv() -> list[str]:
    return ["main.py", "--files", "file1.csv", "file2.csv", "--report", "average-gdp"]


@pytest.fixture
def csv_content() -> str:
    return "country,year,gdp\nUnited States,2023,25462\n"


def test_parse_arguments_valid(valid_argv):
    with patch.object(sys, "argv", valid_argv):
        args = parse_arguments()

        assert args.files == ["file1.csv", "file2.csv"]
        assert args.report == "average-gdp"


@pytest.mark.parametrize("invalid_report", ["unknown-report", "bad", "avg-gdp"])
def test_parse_arguments_invalid_report(invalid_report):
    test_args = ["main.py", "--files", "file1.csv", "--report", invalid_report]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            parse_arguments()


def test_read_csv_files_success(csv_content):
    with patch("builtins.open", mock_open(read_data=csv_content)):
        data = read_csv_files(["dummy_path.csv"])

        assert len(data) == 1
        assert data[0]["country"] == "United States"
        assert data[0]["gdp"] == "25462"


def test_read_csv_files_not_found(caplog):
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(SystemExit) as exc_info:
            read_csv_files(["non_existent.csv"])

        assert exc_info.value.code == 1
    assert "File not found" in caplog.text
