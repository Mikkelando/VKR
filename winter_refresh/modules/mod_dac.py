import numpy as np

# Константы и параметры
CO2toC = 0.27  # Конверсия из CO2 в углерод
years = range(2015, 2101)  # Временной диапазон (пример)
regions = ['Region1', 'Region2', 'Region3']  # Регионы (пример)
tlen = {year: 1 for year in years}  # Длина временных шагов
dac_tot0 = 453 * 1e-3  # Начальная стоимость DAC [T$/GtonCO2]
dac_totfloor = 100 * 1e-3  # Минимальная стоимость DAC [T$/GtonCO2]
capex = 0.4  # Доля инвестиций в стоимости DAC
lifetime = 20  # Срок службы DAC
dac_delta_en = 1 - np.exp(1 / (-lifetime + (0.01 / 2) * lifetime**2))
mkt_growth_rate_dac = {year: {region: 0.06 for region in regions} for year in years}
mkt_growth_free_dac = {year: {region: 0.001 / 5 for region in regions} for year in years}
dac_learn = {year: {region: 0.136 for region in regions} for year in years}
E_NEG = {year: {region: 0 for region in regions} for year in years}
I_CDR = {year: {region: 0 for region in regions} for year in years}
COST_CDR = {year: {region: 0 for region in regions} for year in years}
REV_CDR = {year: {region: 0 for region in regions} for year in years}
GOVSUR = {year: {region: 0 for region in regions} for year in years}
wcum_dac = {year: 0 for year in years}
dac_totcost = {year: {region: dac_tot0 for region in regions} for year in years}

# Этап конфигурации
def configure_dac():
    global dac_tot0, dac_totfloor, capex, lifetime, dac_delta_en
    dac_tot0 = 453 * 1e-3
    dac_totfloor = 100 * 1e-3
    capex = 0.4
    lifetime = 20
    dac_delta_en = 1 - np.exp(1 / (-lifetime + (0.01 / 2) * lifetime**2))

# Этап уравнений
def compute_equations():
    for t in years:
        for n in regions:
            # Уравнение депрессии мощности DAC
            if t < max(years):
                E_NEG[t + 1][n] = (
                    E_NEG[t][n] * (1 - dac_delta_en) ** tlen[t]
                    + tlen[t] * I_CDR[t][n] / (capex * lifetime * dac_totcost[t][n])
                )
            # Уравнение общей стоимости DAC
            COST_CDR[t][n] = (
                I_CDR[t][n]
                + E_NEG[t][n] * dac_totcost[t][n] * (1 - capex)
            )
            # Уравнение доходов DAC
            REV_CDR[t][n] = 100 * E_NEG[t][n]  # Примерная цена углерода

# Перед решением
def before_solve():
    for t in years:
        if t > min(years):
            wcum_dac[t] = tlen[t - 1] * sum(E_NEG[t - 1][n] for n in regions) + wcum_dac[t - 1]
            for n in regions:
                dac_totcost[t][n] = max(
                    dac_tot0 * (wcum_dac[t] / wcum_dac[min(years)]) ** (-dac_learn[t][n]),
                    dac_totfloor,
                )

# Основная функция выполнения модуля
def run_dac_module():
    configure_dac()
    before_solve()
    compute_equations()

# Запуск модуля
if __name__ == "__main__":
    run_dac_module()

    # Вывод результатов
    print("Кумулятивные мощности DAC:", wcum_dac)
    print("Общая стоимость DAC:", dac_totcost)
    print("Установленные мощности DAC (E_NEG):", E_NEG)
    print("Инвестиции DAC (I_CDR):", I_CDR)
    print("Общая стоимость (COST_CDR):", COST_CDR)
    print("Доходы DAC (REV_CDR):", REV_CDR)
