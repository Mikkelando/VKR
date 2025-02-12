def setup_climate(config, emissions):
    """
    Настройка климатической модели.
    """
    climate = {
        'global_temp': 0,
        'emissions': emissions,
    }
    return climate
