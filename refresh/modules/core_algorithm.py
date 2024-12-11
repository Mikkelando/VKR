# ========================== CORE ALGORITHM ==========================
# Define settings, sets, and variables for the solving procedure

class Config:
    def __init__(self):
        # Convergence settings
        self.maxiter = 100
        self.miniter = 4
        self.convergence_tolerance = 1e-1
        self.max_seconds = 3600  # 1 hour
        self.max_solretry = 100


class Sets:
    def __init__(self, maxiter):
        # Sets for solving procedure
        self.iter = [f"i{i}" for i in range(1, maxiter + 1)]
        self.v = ["MIU", "S"]
        self.vcheck = ["MIU", "S"]
        self.clt_problem = []  # List of unsolved coalitions
        self.irep = ["solvestat", "modelstat", "ok"]


class Parameters:
    def __init__(self, iterations, variables):
        # Initialize parameters
        self.converged = 0  # 1 if model converged, 0 otherwise
        self.viter = self.initialize_viter(iterations, variables)
        self.allerr = self.initialize_allerr(iterations, variables)
        self.max_solution_change = 0
        self.max_solution_change_iter = {}
        self.h = {}
        self.solrep = {}
        self.solretry = {}
        self.timer = 0

    @staticmethod
    def initialize_viter(iterations, variables):
        """
        Initialize tracking for utility values.
        """
        return {iter_: {v: {} for v in variables} for iter_ in iterations}

    @staticmethod
    def initialize_allerr(iterations, variables):
        """
        Initialize tracking for remaining differences/errors.
        """
        return {iter_: {v: None for v in variables} for iter_ in iterations}


class GDXItems:
    def __init__(self):
        self.viter = {}
        self.allerr = {}
        self.max_solution_change_iter = {}
        self.solrep = {}
        self.converged = 0
        self.elapsed = 0


# ========================== MAIN EXECUTION ==========================
def main():
    phase = 'conf'  # Change this to 'sets' or 'gdx_items' as needed

    if phase == 'conf':
        config = Config()
        print("Configuration:")
        print(f"Max Iterations: {config.maxiter}")
        print(f"Minimum Iterations: {config.miniter}")
        print(f"Convergence Tolerance: {config.convergence_tolerance}")
        print(f"Max Time (seconds): {config.max_seconds}")
        print(f"Max Solution Retry: {config.max_solretry}")

    elif phase == 'sets':
        maxiter = 100  # Example max iterations
        sets = Sets(maxiter)
        print("Sets:")
        print(f"Iterations: {sets.iter}")
        print(f"Variables: {sets.v}")
        print(f"Variables to Check: {sets.vcheck}")
        print(f"Report Items: {sets.irep}")

    elif phase == 'gdx_items':
        iterations = [f"i{i}" for i in range(1, 101)]
        variables = ["MIU", "S"]
        params = Parameters(iterations, variables)
        print("Parameters and GDX Items Initialized")
        print(f"Converged: {params.converged}")
        print(f"Viter Structure: {params.viter}")
        print(f"All Errors Structure: {params.allerr}")

if __name__ == "__main__":
    main()
