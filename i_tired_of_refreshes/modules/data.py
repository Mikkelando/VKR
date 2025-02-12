import pandas as pd

def load_data(data_path):
    """
    Загрузка данных модели.
    """
    return {
        'regions': pd.read_csv(f"{data_path}/regions.csv"),
        'economy': pd.read_csv(f"{data_path}/economy.csv"),
        'emissions': pd.read_csv(f"{data_path}/emissions.csv"),
    }