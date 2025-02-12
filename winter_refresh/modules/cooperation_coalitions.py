import os

# Глобальные переменные для управления параметрами
PHASE = 'conf'  # Возможные значения: 'conf', 'sets', 'before_solve', 'gdx_items'
REGION_WEIGHTS = 'pop'  # Возможные значения: 'pop', 'negishi'
COALITION_FOLDER = None
DATAPATH = './data/'  # Путь к данным
COALITIONS = {}

def configure_coalitions():
    """Настройка параметров коалиций и других глобальных настроек."""
    global COALITIONS

    gdxfix = "results_default"
    coalitions_t_sequence = 1
    solmode = 'noncoop'

    if REGION_WEIGHTS == 'negishi':
        calc_nweights = "(CPC[t][n] ** elasmu) / sum((CPC[t][nn] ** elasmu) for nn in regions)"
    elif REGION_WEIGHTS == 'pop':
        calc_nweights = "1"
    else:
        calc_nweights = None

    COALITIONS['config'] = {
        "gdxfix": gdxfix,
        "coalitions_t_sequence": coalitions_t_sequence,
        "solmode": solmode,
        "calc_nweights": calc_nweights,
    }

    print("Configuration phase complete.")


def define_sets():
    """Определение наборов коалиций."""
    global COALITIONS

    # Предопределенные коалиции
    COALITIONS['sets'] = {
        "clt": [
            "eu27", "noneu27", "grand", "srm_coalition",
            "coal_a", "coal_b", "coal_c", "coal_d", "coal_e"
        ],
        "map_clt_n": {
            "eu27": ["aut", "bel", "bgr", "cro", "dnk", "esp", "fin", "fra", "grc", "hun", "irl", "ita", "nld", "pol", "prt", "rcz", "rfa", "rom", "rsl", "slo", "swe", "blt"],
            "noneu27": ["gbr", "arg", "aus", "bra", "can", "chl", "chn", "cor", "egy", "golf57", "idn", "jpn", "meme", "mex", "mys", "nde", "noan", "noap", "nor", "osea", "rcam", "ris", "rjan57", "rsaf", "rsam", "rsas", "rus", "sui", "tha", "tur", "ukr", "usa", "vnm", "zaf", "oeu"],
            "grand": [
                "aut", "bel", "bgr", "cro", "dnk", "esp", "fin", "fra", "grc", "hun", "irl", "ita", "nld", "pol", "prt", "rcz", "rfa", "rom", "rsl", "slo", "swe", "blt",
                "gbr", "arg", "aus", "bra", "can", "chl", "chn", "cor", "egy", "golf57", "idn", "jpn", "meme", "mex", "mys", "nde", "noan", "noap", "nor", "osea", "rcam", "ris", "rjan57", "rsaf", "rsam", "rsas", "rus", "sui", "tha", "tur", "ukr", "usa", "vnm", "zaf", "oeu"
            ],
        }
    }

    # Инициализация флага cltsolve
    COALITIONS['cltsolve'] = {clt: False for clt in COALITIONS['sets']['clt']}
    COALITIONS['cltsolve']['eu27'] = True
    COALITIONS['cltsolve']['noneu27'] = True

    if COALITION_FOLDER:
        coalition_path = os.path.join(DATAPATH, "data_srm_coalition", COALITION_FOLDER)
        # Загрузка дополнительных данных коалиции, если они есть
        COALITIONS['cltsolve'].update(load_coalition_data(coalition_path))

    print("Sets phase complete.")


def load_coalition_data(folder_path):
    """Загрузка данных для коалиций из указанной папки."""
    coalition_data = {}
    try:
        with open(os.path.join(folder_path, "cltsolve.inc"), "r") as f:
            for line in f:
                clt = line.strip()
                coalition_data[clt] = True
    except FileNotFoundError:
        print("No additional coalition data found.")
    return coalition_data


def before_solve():
    """Действия перед запуском решения."""
    print("Performing pre-solve actions...")
    # Здесь можно добавить логику подготовки перед решением


def generate_gdx_items():
    """Генерация GDX-объектов."""
    print("Generating GDX items...")
    gdx_items = {
        "clt": COALITIONS['sets']['clt'],
        "map_clt_n": COALITIONS['sets']['map_clt_n'],
        "cltsolve": COALITIONS['cltsolve'],
    }
    print("GDX items generated.")
    return gdx_items


def main():
    """Главная функция для управления фазами."""
    if PHASE == 'conf':
        configure_coalitions()
    elif PHASE == 'sets':
        define_sets()
    elif PHASE == 'before_solve':
        before_solve()
    elif PHASE == 'gdx_items':
        generate_gdx_items()
    else:
        raise ValueError(f"Unknown phase: {PHASE}")


if __name__ == "__main__":
    main()
