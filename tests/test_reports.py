import pytest

from reports import AverageGdpReport


@pytest.fixture
def report() -> AverageGdpReport:
    return AverageGdpReport()


@pytest.fixture
def sample_data() -> list[dict]:
    return [
        {"country": "United States", "gdp": "25000"},
        {"country": "United States", "gdp": "20000"},
        {"country": "China", "gdp": "18000"},
        {"country": "China", "gdp": "16000"},
        {"country": "Germany", "gdp": "4000"},
    ]


def test_average_gdp_report_calculation(report, sample_data):
    result = report.generate(sample_data)

    assert len(result) == 3
    assert result[0] == ["United States", 22500.0]
    assert result[1] == ["China", 17000.0]
    assert result[2] == ["Germany", 4000.0]


def test_average_gdp_report_headers(report):
    assert report.get_headers() == ["Country", "Average GDP"]


@pytest.mark.parametrize(
    "missing_data, expected_len, expected_country, expected_gdp",
    [
        (
            [
                {"country": "United States", "gdp": "25000"},
                {"country": "United States", "gdp": ""},
                {"gdp": "10000"},
            ],
            1,
            "United States",
            25000.0,
        ),
        (
            [{"country": "", "gdp": "10000"}, {"gdp": "5000"}],
            0,
            None,
            None,
        ),
    ],
)
def test_average_gdp_report_missing_data(
    report, missing_data, expected_len, expected_country, expected_gdp
):
    result = report.generate(missing_data)

    assert len(result) == expected_len
    if expected_len > 0:
        assert result[0][0] == expected_country
        assert result[0][1] == expected_gdp
