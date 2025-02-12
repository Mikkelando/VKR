def setup_emissions(emissions_data, economy, config):
    """
    Настройка данных по выбросам.
    """
    emissions = {
        region: emissions_data[emissions_data['region'] == region]
        for region in economy.keys()
    }
    return emissions
