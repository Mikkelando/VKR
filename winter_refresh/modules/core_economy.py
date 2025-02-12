class CoreEconomy:
    def __init__(self):
        # Конфигурации
        self.global_savings = "fixed"  # Опции: 'fixed' или 'flexible'
        self.update_ssp_by_historical = False  # Использовать ли исторические данные для обновления SSP
        self.default_prstp = 0.015  # Базовая норма временных предпочтений
        self.default_elasmu = 1.45  # Коэффициент межвременной эластичности замещения
        self.default_savings = "fixed"  # Режим сбережений
        self.exchange_rate = "PPP"  # Тип курса: 'PPP' или 'MER'

        # Наборы
        self.ssp_baselines = ["ssp1", "ssp2", "ssp3", "ssp4", "ssp5"]
        self.gdp_adjustment_types = ["PPP", "MER"]
        self.production_factors = ["labour", "capital"]

        # Параметры
        self.depreciation_rate = 0.1  # Годовая норма амортизации капитала
        self.prodshare = {"labour": 0.7, "capital": 0.3}  # Доли факторов в функции Кобба-Дугласа
        self.dice_opt_savings = 0.2751  # Оптимальная норма сбережений из DICE2016

        # Данные для загрузки
        self.ykali = {}  # ВВП для динамической калибровки [трлн долл.]
        self.l = {}  # Население [млн человек]
        self.pop = {}  # Население [млн человек]
        self.gdppc_kali = {}  # ВВП на душу населения для калибровки [MER]

        # Переменные
        self.variables = {}

    def configure_economy(self):
        """Конфигурация экономики."""
        print(f"[CoreEconomy] Конфигурация экономики: global_savings={self.global_savings}, exchange_rate={self.exchange_rate}")

    def define_sets(self):
        """Определение наборов."""
        print(f"[CoreEconomy] Определены базовые сценарии SSP: {self.ssp_baselines}")

    def include_data(self):
        """Загрузка данных."""
        print("[CoreEconomy] Загрузка данных экономики (SSP, население, ВВП и т.д.)")

    def compute_data(self):
        """Вычисление данных."""
        print("[CoreEconomy] Вычисление экономических параметров (рост ВВП, базовые нормы сбережений и т.д.)")

    def declare_vars(self):
        """Объявление переменных."""
        print("[CoreEconomy] Объявление переменных экономики (C, Y, I, S и др.)")

    def compute_vars(self):
        """Вычисление переменных."""
        print("[CoreEconomy] Вычисление значений переменных экономики на основе модели")


# -------------------------------------------------
# Глобальная функция handle_phase
# -------------------------------------------------
def handle_phase(phase, *args, **kwargs):
    """
    Глобальная функция, которая создаёт экземпляр CoreEconomy 
    и вызывает соответствующие методы в зависимости от переданной фазы.
    """
    economy = CoreEconomy()

    phase_methods = {
        "conf": economy.configure_economy,
        "sets": economy.define_sets,
        "include_data": economy.include_data,
        "compute_data": economy.compute_data,
        "declare_vars": economy.declare_vars,
        "compute_vars": economy.compute_vars
    }

    if phase in phase_methods:
        phase_methods[phase]()
    else:
        print(f"[CoreEconomy] Неизвестная фаза: {phase}")


# ========================== MAIN EXECUTION ==========================
if __name__ == "__main__":
    # Пример использования handle_phase
    handle_phase("conf")
    handle_phase("sets")
    handle_phase("include_data")
    handle_phase("compute_data")
    handle_phase("declare_vars")
    handle_phase("compute_vars")
