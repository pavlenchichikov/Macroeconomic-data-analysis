import argparse
import csv
import sys
from typing import List, Dict
from tabulate import tabulate
from reports import REPORTS_REGISTRY

def parse_arguments() -> argparse.Namespace:
    # Инициализируем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Macroeconomic data analyzer script")
    
    # Добавляем аргумент --files, который принимает один или несколько файлов
    parser.add_argument(
        "--files", 
        nargs="+", 
        required=True, 
        help="Paths to the input CSV files."
    )
    
    # Добавляем аргумент --report, список допустимых значений берем из ключей реестра
    parser.add_argument(
        "--report", 
        required=True, 
        choices=list(REPORTS_REGISTRY.keys()), 
        help="The name of the report to generate."
    )
    
    return parser.parse_args()

def read_csv_files(file_paths: List[str]) -> List[Dict[str, str]]:
    # Инициализируем пустой список для хранения всех данных в памяти
    all_data = []
    
    # Итерируемся по списку переданных путей к файлам
    for file_path in file_paths:
        try:
            # Открываем файл для чтения
            with open(file_path, mode="r", encoding="utf-8") as f:
                # Используем csv.DictReader, чтобы каждая строка была словарем (ключи - заголовки)
                reader = csv.DictReader(f)
                for row in reader:
                    all_data.append(row)
        except FileNotFoundError:
            # Обрабатываем ситуацию, когда файл не найден, выводим ошибку в stderr и прерываем выполнение
            print(f"Error: File not found - {file_path}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            # Перехват непредвиденных ошибок чтения (например, нет прав доступа)
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            sys.exit(1)
            
    return all_data

def main():
    # 1. Получаем аргументы от пользователя
    args = parse_arguments()
    
    # 2. Читаем данные из всех переданных файлов
    data = read_csv_files(args.files)
    
    # Проверка на наличие данных. Если файлы пусты, сообщаем об этом
    if not data:
        print("Warning: No data found in the provided files.")
        sys.exit(0)
        
    # 3. Достаем нужный отчет из реестра
    report_strategy = REPORTS_REGISTRY[args.report]
    
    # 4. Генерируем результаты отчета
    report_data = report_strategy.generate(data)
    headers = report_strategy.get_headers()
    
    # 5. Выводим результат в консоль с помощью tabulate
    # tablefmt="grid" делает таблицу визуально читаемой
    print(tabulate(report_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()