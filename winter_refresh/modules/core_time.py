# modules/core_time.py

class CoreTime:
    def __init__(self):
        # Global configurations
        self.tfix = 1

        # Time period sets and parameters
        self.time_periods = []  # Placeholder for loading from time.inc
        self.tstep = 5
        self.tfirst = set()
        self.tsecond = set()
        self.tlast = set()
        self.last10 = set()
        self.tfix = set()
        self.precedence = {}
        self.predecessors = {}
        self.tperiod = {}
        self.year = {}
        self.begyear = {}
        self.tlen = {}

    def load_time_periods(self, time_data):
        """Load time periods from external data."""
        self.time_periods = time_data
        self.define_time_controls()

    def define_time_controls(self):
        """Define temporal control sets based on loaded time periods."""
        total_periods = len(self.time_periods)
        
        for i, t in enumerate(self.time_periods, start=1):
            self.tperiod[t] = i
            if i == 1:
                self.tfirst.add(t)
            if i == 2:
                self.tsecond.add(t)
            if i == total_periods:
                self.tlast.add(t)
            if i > total_periods - 10:
                self.last10.add(t)

    def set_fixed_periods(self, tfix_threshold):
        """Set fixed periods based on threshold."""
        self.tfix = {t for t, period in self.tperiod.items() if period <= tfix_threshold}

    def load_fix_variable(self, name, idx, data):
        """Load fixed variable data."""
        return data.get(name, {}).get(idx, None)

    def apply_fix_variable(self, name, idx, data):
        """Apply fixed variable logic for tfix periods."""
        fixed_value = self.load_fix_variable(name, idx, data)
        if fixed_value is not None:
            for t in self.tfix:
                # Example logic to apply fixed values
                print(f"Applying fixed value {fixed_value} for {name}[{idx}] in period {t}")

    def report(self):
        """Report sets and parameters for debugging or exporting."""
        print("Time periods:", self.time_periods)
        print("First period:", self.tfirst)
        print("Second period:", self.tsecond)
        print("Last period:", self.tlast)
        print("Last 10 periods:", self.last10)
        print("Fixed periods:", self.tfix)
        print("Time step:", self.tstep)
        print("Period mapping:", self.tperiod)
        print("Year mapping:", self.year)


# -------------------------------------------------
# Глобальная функция handle_phase
# -------------------------------------------------
def handle_phase(phase, arg2=None):
    """
    Глобальная функция, которую можно вызывать как:
       from modules.core_time import handle_phase
       ...
       handle_phase("conf")
    Внутри создаём объект CoreTime и вызываем нужные методы 
    в зависимости от 'phase'.
    """

    # Можно хранить объект CoreTime в глобальной переменной (необязательно),
    # но для простоты создадим новый объект на каждый вызов:
    core_time_obj = CoreTime()

    if phase == "conf":
        print("[core_time] Handling 'conf' phase")
        # Здесь можно инициализировать или сбросить что-то, 
        # либо просто заглушка.

    elif phase == "sets":
        print("[core_time] Handling 'sets' phase")
        # Пример: загружаем тестовые периоды (или из arg2?)
        # Здесь можно вызывать core_time_obj.load_time_periods(...)
        test_periods = ["2020", "2025", "2030", "2035", "2040"]
        core_time_obj.load_time_periods(test_periods)

    elif phase == "include_data":
        print("[core_time] Handling 'include_data' phase")
        # Если нужно, подгрузка дополнительных данных

    elif phase == "compute_data":
        print("[core_time] Handling 'compute_data' phase")
        # Пример: core_time_obj.set_fixed_periods(3) (для теста)
        core_time_obj.set_fixed_periods(3)

    elif phase == "declare_vars":
        print("[core_time] Handling 'declare_vars' phase")
        # Логика объявления переменных

    elif phase == "compute_vars":
        print("[core_time] Handling 'compute_vars' phase")
        # Пример применения fixed variable
        fake_data = {"var_name": {"idx": 42}}
        core_time_obj.apply_fix_variable("var_name", "idx", fake_data)

    elif phase == "report":
        print("[core_time] Handling 'report' phase")
        core_time_obj.report()

    else:
        print(f"[core_time] No specific logic for phase '{phase}'")


# Для отладки
if __name__ == "__main__":
    # Пример использования напрямую
    handle_phase("conf")
    handle_phase("sets")
    handle_phase("compute_data")
    handle_phase("declare_vars")
    handle_phase("compute_vars")
    handle_phase("report")
