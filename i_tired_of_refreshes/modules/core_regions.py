import pandas as pd

def setup_regions(region_data, config):
    """
    Настройка регионов для модели.
    """
    regions = region_data['region'].tolist()
    active_regions = config.get('only_solve', regions)
    return {
        'all_regions': regions,
        'active_regions': [r for r in regions if r in active_regions],
    }
