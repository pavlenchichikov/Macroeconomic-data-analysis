import pytest
import sys
from unittest.mock import patch, mock_open
from main import parse_arguments, read_csv_files

def test_parse_arguments_valid():
    # Подменяем аргументы командной строки
    test_args = ["main.py", "--files", "file1.csv", "file2.csv", "--report", "average-gdp"]
    with patch.object(sys, 'argv', test_args):
        args = parse_arguments()
        
        # Проверяем, что парсер корректно распознал файлы и название отчета
        assert args.files == ["file1.csv", "file2.csv"]
        assert args.report == "average-gdp"

def test_parse_arguments_invalid_report():
    # Проверяем, что при неверном названии отчета скрипт завершается с ошибкой
    test_args = ["main.py", "--files", "file1.csv", "--report", "unknown-report"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            parse_arguments()

def test_read_csv_files_success():
    # Имитируем содержимое CSV файла (заголовки + одна строка)
    csv_content = "country,year,gdp\nUnited States,2023,25462\n"
    
    # Подменяем функцию open, чтобы не читать реальный файл с диска
    with patch("builtins.open", mock_open(read_data=csv_content)):
        data = read_csv_files(["dummy_path.csv"])
        
        # Проверяем корректность парсинга
        assert len(data) == 1
        assert data[0]["country"] == "United States"
        assert data[0]["gdp"] == "25462"

def test_read_csv_files_not_found(capsys):
    # Проверяем реакцию системы на отсутствие файла
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(SystemExit) as exc_info:
            read_csv_files(["non_existent.csv"])
        
        # Скрипт должен завершиться с кодом 1
        assert exc_info.value.code == 1
        
        # Проверяем вывод текста ошибки
        captured = capsys.readouterr()
        assert "Error: File not found" in captured.err