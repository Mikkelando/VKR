import os
from gdxpds.gdx import GdxFile

def convert_gdx_to_csv(input_folder, output_folder):
    """
    Конвертирует все файлы .gdx в указанной директории в .csv и сохраняет в output_folder.
    
    :param input_folder: Путь к папке с .gdx файлами.
    :param output_folder: Путь к папке для сохранения .csv файлов.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".gdx"):
            gdx_path = os.path.join(input_folder, file_name)
            csv_name = file_name.replace(".gdx", ".csv")
            csv_path = os.path.join(output_folder, csv_name)
            
            try:
                with GdxFile(gdx_path) as gdx:
                    df = gdx.to_dataframe()
                    df.to_csv(csv_path, index=False)
                    print(f"Успешно конвертирован: {file_name} -> {csv_name}")
            except Exception as e:
                print(f"Ошибка при конвертации {file_name}: {e}")

if __name__ == "__main__":
    input_folder = "data/data_ed57"  # Укажите путь к папке с .gdx файлами
    output_folder = "data/data_csv"  # Укажите путь для сохранения .csv файлов
    convert_gdx_to_csv(input_folder, output_folder)
