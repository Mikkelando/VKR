def handle_phase(phase, t_vals=None, n_vals=None):
    """
    Глобальная функция для обработки этапов модуля core_welfare.
    :param phase: Этап ('conf', 'sets', 'include_data', 'compute_data', 'declare_vars' или 'compute_vars').
    :param t_vals: Список временных интервалов (может быть None).
    :param n_vals: Список регионов (может быть None).
    """
    welfare_module = WelfareModule()

    if phase == "conf":
        print("[core_welfare] Configuring welfare module")
    elif phase == "compute_data":
        print("[core_welfare] Computing data")
        if t_vals is None or n_vals is None:
            raise ValueError("[core_welfare] t_vals and n_vals must not be None for compute_data phase.")
        welfare_module.compute_data(t_vals, n_vals)
    elif phase == "declare_vars":
        print("[core_welfare] Declaring variables")
        if t_vals is None or n_vals is None:
            raise ValueError("[core_welfare] t_vals and n_vals must not be None for declare_vars phase.")
        welfare_module.declare_variables(t_vals, n_vals)
    elif phase == "compute_vars":
        print("[core_welfare] Computing variables")
        if t_vals is None:
            raise ValueError("[core_welfare] t_vals must not be None for compute_vars phase.")
        welfare_module.compute_variables(t_vals)
    elif phase == "report":
        print("[core_welfare] Reporting data")
        welfare_module.report()
    else:
        print(f"[core_welfare] Unknown phase: {phase}")


class WelfareModule:
    def __init__(self, swf='disentangled', prstp=0.015, elasmu=1.45, gamma=0.5, gdpadjust='PPP', dice_scale1=1e-4, dice_scale2=0):
        # User-configurable parameters
        self.swf = swf
        self.prstp = prstp
        self.elasmu = elasmu
        self.gamma = gamma
        self.gdpadjust = gdpadjust
        self.dice_scale1 = dice_scale1
        self.dice_scale2 = dice_scale2

        # Weights and utility parameters initialized
        self.nweights = {}  # nweights(t, n)
        self.rr = {}        # rr(t)
        self.welfare_bge = {}  # welfare_bge(n)
        self.welfare_regional = {}  # welfare_regional(n)
        self.UTILITY = 0  # Initialize utility as 0
        self.TUTILITY = {}  # Initialize TUTILITY dictionary

    def compute_data(self, tsteps, t_vals):
        if tsteps is None or t_vals is None:
            raise ValueError("[core_welfare] tsteps and t_vals must not be None in compute_data.")

        # WEIGHTS
        for t in tsteps:
            for n in t_vals:
                self.nweights[(t, n)] = 1

        # DISCOUNT FACTOR
        for t in tsteps:
            self.rr[t] = 1 / ((1 + self.prstp) ** (t * (t - 1)))

    def declare_variables(self, t_vals, n_vals):
        if t_vals is None or n_vals is None:
            raise ValueError("[core_welfare] t_vals and n_vals must not be None in declare_variables.")

        self.PERIODU = {}  # PERIODU(t, n)
        self.CEMUTOTPER = {}  # CEMUTOTPER(t, n)
        self.TUTILITY = {t: 0 for t in t_vals}  # Initialize TUTILITY with default values
        self.UTARG = {}  # UTARG(t, n)

    def compute_variables(self, tsteps):
        if tsteps is None:
            raise ValueError("[core_welfare] tsteps must not be None in compute_variables.")

        for t in tsteps:
            self.TUTILITY[t] = 0.001  # Dummy computation for demonstration

    def report(self):
        print(f"Welfare BGE: {self.welfare_bge}")
        print(f"Welfare Regional: {self.welfare_regional}")
        print(f"Utility: {self.UTILITY}")


if __name__ == "__main__":
    # Example usage
    t_vals = [1, 2, 3]
    n_vals = ['A', 'B']
    handle_phase("conf")
    handle_phase("compute_data", t_vals, n_vals)
    handle_phase("declare_vars", t_vals, n_vals)
    handle_phase("compute_vars", t_vals)
    handle_phase("report")
