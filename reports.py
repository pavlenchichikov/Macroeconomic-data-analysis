import abc
from typing import List, Dict, Any

# Базовый абстрактный класс для всех отчетов. 
# Гарантирует, что любой новый отчет будет иметь нужные методы.
class BaseReport(abc.ABC):
    @abc.abstractmethod
    def generate(self, data: List[Dict[str, str]]) -> List[List[Any]]:
        # Метод должен принимать список словарей (строки из CSV)
        # и возвращать список списков (строки для таблицы tabulate)
        pass

    @abc.abstractmethod
    def get_headers(self) -> List[str]:
        # Метод должен возвращать заголовки для колонок таблицы
        pass

# Реализация конкретного отчета для расчета среднего ВВП
class AverageGdpReport(BaseReport):
    def generate(self, data: List[Dict[str, str]]) -> List[List[Any]]:
        # Словари для накопления суммы ВВП и количества записей по каждой стране
        gdp_sum_by_country: Dict[str, float] = {}
        count_by_country: Dict[str, int] = {}

        # Проходим по всем переданным строкам данных
        for row in data:
            country = row.get("country")
            # Если поле gdp пустое или отсутствует, пропускаем итерацию, 
            # чтобы избежать ошибок преобразования типов
            if not country or not row.get("gdp"):
                continue

            # Преобразуем значение ВВП в число с плавающей точкой
            gdp_value = float(row["gdp"])

            # Накапливаем сумму и количество
            if country in gdp_sum_by_country:
                gdp_sum_by_country[country] += gdp_value
                count_by_country[country] += 1
            else:
                gdp_sum_by_country[country] = gdp_value
                count_by_country[country] = 1

        # Формируем итоговый список для вывода
        results = []
        for country, total_gdp in gdp_sum_by_country.items():
            # Рассчитываем среднее арифметическое
            average_gdp = total_gdp / count_by_country[country]
            results.append([country, average_gdp])

        # Сортируем результат по среднему ВВП (индекс 1) по убыванию (reverse=True)
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def get_headers(self) -> List[str]:
        # Возвращаем названия колонок для этого отчета
        return ["Country", "Average GDP"]

# Реестр отчетов. 
# Для добавления нового отчета нужно написать класс (наследуя BaseReport) 
# и добавить его сюда в виде пары "название-из-консоли": ЭкземплярКласса().
REPORTS_REGISTRY = {
    "average-gdp": AverageGdpReport(),
}