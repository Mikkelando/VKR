# import sys
# sys.path.append('./')


from modules.core_regions import setup_regions
from modules.core_economy import setup_economy
from modules.core_emissions import setup_emissions
from modules.hub_climate import setup_climate
from modules.optimization_loop import optimization_loop
from config import load_config
from modules.data import load_data 

def main():
    # Загрузка конфигурации и данных
    config = load_config()
    data = load_data(config['data_path'])

    # Настройка регионов
    regions = setup_regions(data['regions'], config)
    
    # Настройка экономики
    economy = setup_economy(data['economy'], regions, config)
    
    # Настройка выбросов
    emissions = setup_emissions(data['emissions'], economy, config)
    
    # Настройка климата
    climate = setup_climate(config, emissions)

    # Запуск цикла оптимизации
    results = optimization_loop(config['t_sequence'], economy, climate, config)

    # Сохранение результатов
    with open(f"{config['results_path']}/summary.txt", "w") as f:
        f.write(str(results))
    
    print("Модель успешно завершена!")

if __name__ == "__main__":
    main()
