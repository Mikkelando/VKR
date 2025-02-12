def setup_economy(economy_data, regions, config):
    """
    Настройка экономической модели.
    """
    economy = {
        region: economy_data[economy_data['region'] == region]
        for region in regions['active_regions']
    }
    return economy
