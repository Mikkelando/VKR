from modules.equations import economic_growth, emissions_calculation, temperature_change

def optimization_loop(t_sequence, economy, climate, config):
    """
    Цикл оптимизации.
    """
    results = {}
    global_temp = climate['global_temp']

    for t in t_sequence:
        print(f"Оптимизация для шага {t}...")

        def objective_function(x):
            # x = [инвестиции, интенсивность выбросов]
            investment, emissions_intensity = x
            
            # Расчёт экономического роста
            gdp = economic_growth(
                economy['gdp'][t - 1],
                investment,
                economy['depreciation'][t - 1]
            )

            # Расчёт выбросов
            emissions = emissions_calculation(gdp, emissions_intensity)

            # Изменение температуры
            temperature = temperature_change(global_temp, emissions, climate['sensitivity'])

            # Потери от ущерба (например, через функции ущерба)
            damages = emissions * 0.01  # Условное значение ущерба

            # Целевая функция: максимизация полезности или минимизация ущерба
            return - (gdp - damages)

        # Начальные значения
        initial_guess = [1.0, 0.5]  # Инвестиции, интенсивность выбросов

        # Решение задачи оптимизации
        from scipy.optimize import minimize
        result = minimize(objective_function, initial_guess, bounds=[(0, None), (0, 1)])

        # Сохранение результатов
        results[t] = {
            'investment': result.x[0],
            'emissions_intensity': result.x[1],
            'objective_value': -result.fun
        }

        # Обновление состояния
        global_temp = temperature_change(global_temp, result.x[1], climate['sensitivity'])

    return results
