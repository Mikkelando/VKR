# modules/equations.py

def economic_growth(gdp, investment, depreciation):
    """
    Экономический рост: Y(t+1) = Y(t) + Investment - Depreciation
    """
    return gdp + investment - depreciation

def emissions_calculation(economic_output, emissions_intensity):
    """
    Вычисление выбросов: Emissions = GDP * Emissions Intensity
    """
    return economic_output * emissions_intensity

def temperature_change(global_temp, emissions, climate_sensitivity):
    """
    Изменение температуры: ΔT = sensitivity * log(emissions)
    """
    import numpy as np
    return global_temp + climate_sensitivity * np.log(emissions + 1)

def welfare(consumption, discount_rate, population):
    """
    Полезность (Welfare): U = Σ (C^(1-θ) - 1) / (1 - θ)
    """
    theta = 2.0  # Коэффициент риска
    return sum([(c**(1 - theta) - 1) / (1 - theta) for c in consumption]) * discount_rate * population
