def calculate_welfare(consumption, discount_rate, population):
    """
    Полезность (Welfare): Σ (C^(1-θ) - 1) / (1 - θ)
    """
    theta = 2.0  # Коэффициент риска
    welfare = sum([
        ((c**(1 - theta) - 1) / (1 - theta)) * discount_rate
        for c in consumption
    ])
    return welfare * population
