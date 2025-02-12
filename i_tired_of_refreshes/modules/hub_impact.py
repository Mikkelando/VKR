def climate_damage(temperature, gdp):
    """
    Ущерб от изменения климата: D = GDP * DamageFactor
    """
    damage_factor = 0.01 * (temperature**2)  # Условная зависимость
    return gdp * damage_factor
