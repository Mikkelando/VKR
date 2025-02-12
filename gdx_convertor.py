from gamspy import Container
import pandas as pd
import os

def gdx_to_csv(gdx_file, output_folder="converted_data"):
    """
    Конвертирует все параметры из GDX в CSV-файлы.
    
    Параметры:
    - gdx_file (str): Путь к GDX-файлу
    - output_folder (str): Папка для сохранённых CSV (по умолчанию "converted_data")
    """
    os.makedirs(output_folder, exist_ok=True)

    # Загружаем GDX
    gdx = Container()
    gdx.read(gdx_file)

    # Получаем список параметров
    symbols = gdx.getSymbols()  # Используем getSymbols() вместо get_symbols()
    
    if not symbols:
        print("⚠️ В GDX нет данных!")
        return
    
    # Извлекаем имена параметров
    param_names = [param.name for param in symbols]

    print(f"🔍 Загружены параметры: {param_names}")

    # Проходим по всем параметрам
    for param_name in param_names:
        param = gdx[param_name]  # Теперь param_name — это строка
        df = pd.DataFrame(param.records)

        if df.empty:
            continue  # Пропускаем пустые параметры

        csv_file = os.path.join(output_folder, f"{param_name}.csv")
        df.to_csv(csv_file, index=False)
        print(f"✅ {param_name} сохранён в {csv_file}")

# 🔥 Запуск конвертации
gdx_to_csv("i_tired_of_refreshes/data/data_ed57/data_baseline.gdx")  # Укажи свой GDX-файл