import abc
from typing import Any, TypedDict


class CountryRow(TypedDict, total=False):
    country: str
    year: str
    gdp: str
    gdp_growth: str
    inflation: str
    unemployment: str
    population: str
    continent: str


class BaseReport(abc.ABC):
    @abc.abstractmethod
    def generate(self, data: list[CountryRow]) -> list[list[Any]]:
        pass

    @abc.abstractmethod
    def get_headers(self) -> list[str]:
        pass


class AverageGdpReport(BaseReport):
    def generate(self, data: list[CountryRow]) -> list[list[Any]]:
        gdp_sum: dict[str, float] = {}
        gdp_count: dict[str, int] = {}

        for row in data:
            country = row.get("country")
            # Skip rows with missing country or gdp to avoid conversion errors
            if not country or not row.get("gdp"):
                continue

            gdp_value = float(row["gdp"])

            if country in gdp_sum:
                gdp_sum[country] += gdp_value
                gdp_count[country] += 1
            else:
                gdp_sum[country] = gdp_value
                gdp_count[country] = 1

        results = [
            [country, gdp_sum[country] / gdp_count[country]]
            for country in gdp_sum
        ]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_headers(self) -> list[str]:
        return ["Country", "Average GDP"]


REPORTS_REGISTRY: dict[str, BaseReport] = {
    "average-gdp": AverageGdpReport(),
}
