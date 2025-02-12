import json
import os
import matplotlib.pyplot as plt

def load_dice_data(json_file="dice_data.json"):
    """
    Загружает данные DICE из JSON-файла.
    
    Параметры:
        json_file (str): Путь к JSON-файлу (по умолчанию "dice_data.json")

    Возвращает:
        dict: Загруженные данные.
    """
    with open(json_file, "r") as f:
        data = json.load(f)
    return data

def save_dice_graphs(json_file="dice_data.json", output_dir="graphs"):
    """
    Строит и сохраняет графики для всех переменных из данных DICE.
    
    Параметры:
        json_file (str): Путь к JSON-файлу с данными (по умолчанию "dice_data.json")
        output_dir (str): Папка для сохранения графиков (по умолчанию "graphs")
    """
    # Загружаем данные
    data = load_dice_data(json_file)
    
    # Создаем папку для графиков, если её нет
    os.makedirs(output_dir, exist_ok=True)
    
    # Шаг по годам
    years = list(range(2020, 2020 + len(next(iter(data.values())).values().__iter__().__next__()) * 5, 5))

    for variable, scenarios in data.items():
        plt.figure(figsize=(10, 6))

        for scenario, values in scenarios.items():
            plt.plot(years, values, label=scenario, linewidth=2)

        # Оформление графика
        plt.title(variable.replace("_", " ").capitalize())
        plt.xlabel("Год")
        plt.ylabel("Значение")
        plt.legend()
        plt.grid(True)
        
        # Сохранение графика
        graph_path = os.path.join(output_dir, f"{variable}.png")
        plt.savefig(graph_path, dpi=300)
        plt.close()

        print(f"✅ График сохранен: {graph_path}")

if __name__ == "__main__":
    save_dice_graphs(output_dir='UI/new_graphs')
    print("🎉 Все графики сохранены в папку graphs/")