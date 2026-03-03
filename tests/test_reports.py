import pytest
from reports import AverageGdpReport

def test_average_gdp_report_calculation():
    # Инициализируем отчет
    report = AverageGdpReport()
    
    # Подготавливаем тестовые данные, имитирующие вывод csv.DictReader
    test_data = [
        {"country": "United States", "gdp": "25000"},
        {"country": "United States", "gdp": "20000"},
        {"country": "China", "gdp": "18000"},
        {"country": "China", "gdp": "16000"},
        {"country": "Germany", "gdp": "4000"}
    ]
    
    # Вызываем метод генерации отчета
    result = report.generate(test_data)
    
    # Проверяем, что результат отсортирован по убыванию ВВП
    # US (22500), China (17000), Germany (4000)
    assert len(result) == 3
    
    assert result[0][0] == "United States"
    assert result[0][1] == 22500.0
    
    assert result[1][0] == "China"
    assert result[1][1] == 17000.0
    
    assert result[2][0] == "Germany"
    assert result[2][1] == 4000.0

def test_average_gdp_report_headers():
    # Проверка того, что отчет возвращает правильные заголовки
    report = AverageGdpReport()
    headers = report.get_headers()
    assert headers == ["Country", "Average GDP"]

def test_average_gdp_report_missing_data():
    # Проверка работы скрипта, если в данных пропущены поля gdp или country
    report = AverageGdpReport()
    test_data = [
        {"country": "United States", "gdp": "25000"},
        {"country": "United States", "gdp": ""}, # Пропущено значение ВВП
        {"gdp": "10000"}, # Пропущена страна
    ]
    
    result = report.generate(test_data)
    
    # Ожидаем только одну успешную запись в итоговой таблице
    assert len(result) == 1
    assert result[0][0] == "United States"
    assert result[0][1] == 25000.0