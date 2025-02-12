import json
from collections import defaultdict
from pathlib import Path
import os

# Настройки модели DICE
START_YEAR = 2020
YEAR_STEP = 5
TOTAL_STEPS = 20  # Например, 100 лет вперед (20 шагов по 5 лет)

def extract_dice_data(until=2100, data_dir="."):
    """
    Функция для извлечения данных из файлов решения DICE и возврата в виде словаря.
    
    Параметры:
        until (int): До какого года загружать данные (по умолчанию 2100)
        data_dir (str): Папка, где хранятся файлы решений DICE (по умолчанию текущая папка)
    
    Возвращает:
        dict: Данные в формате {переменная: {сценарий: [значения по годам]}}
    """
    filenames = [f"{data_dir}/ssp{s}_solution.txt" for s in range(1, 6)] + [f"{data_dir}/reference.txt"]
    years = list(range(START_YEAR, until + YEAR_STEP, YEAR_STEP))

    required_variables = [
        'co2_emission_control', 'ch4_emission_control', 'carbon_price', 
        'co2_reservoir', 'ch4_reservoir', 'population', 'scc', 'scch4'
    ]

    values = defaultdict(dict)
    
    for path in filenames:
        if not os.path.exists(path):
            print(f"⚠️ Файл не найден: {path}")
            continue

        scenario_name = os.path.basename(path)  # Имя файла как ключ сценария

        with open(path) as f:
            for line in f:
                lst = line.strip().split(',')
                var, vals = lst[0], lst[1:]
                if var in required_variables:
                    vals = [float(val) for val in vals]
                    values[var][scenario_name] = vals[:len(years)]

    return values

def save_dice_data(until=2100, output_file="dice_data.json", data_dir="."):
    """
    Функция для сохранения данных DICE в JSON-файл.
    
    Параметры:
        until (int): До какого года загружать данные (по умолчанию 2100)
        output_file (str): Имя файла для сохранения
        data_dir (str): Папка, где хранятся файлы решений DICE
    """
    data = extract_dice_data(until, data_dir)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Данные DICE сохранены в {output_file}")

# Тест запуска, если скрипт запускается напрямую
if __name__ == '__main__':
    save_dice_data(2100, "dice_data.json", data_dir='./dice-ch4/')