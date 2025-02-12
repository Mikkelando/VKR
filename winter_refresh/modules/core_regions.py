def handle_phase(phase, datapath='./data/', only_solve=None):
    """
    Глобальная функция для обработки этапов в RegionModule.
    :param phase: Этап ('conf', 'sets', 'include_data', 'compute_data', или 'gdx_items').
    :param datapath: Путь к данным.
    :param only_solve: Опционально; задаёт единственный регион для обработки.
    """
    module = RegionModule()
    module.handle_phase(phase=phase, datapath=datapath, only_solve=only_solve)


class RegionModule:
    def __init__(self):
        """Initialize default parameters for the region module."""
        self.phase = None
        self.datapath = None
        self.only_solve = None
        self.regions = {}
        self.nsolve = {}
        self.dice_curve = ["original", "discounted"]
        self.trns_type = [
            "linear_pure",
            "linear_soft",
            "sigmoid_HHs",
            "sigmoid_Hs",
            "sigmoid_Ms",
            "sigmoid_Ls",
            "sigmoid_LLs",
        ]
        self.trns_end = [28, 38, 48, 58]

    def load_config(self, datapath):
        """Load configuration data from the specified path."""
        config_path = f"{datapath}regions.conf"
        try:
            with open(config_path, 'r') as file:
                config_data = file.read()
            print("Loaded configuration:", config_data)
        except FileNotFoundError:
            print(f"Configuration file not found at {config_path}. Ensure the file exists.")

    def load_regions(self, datapath):
        """Load region data from the specified path."""
        regions_path = f"{datapath}regions.inc"
        try:
            with open(regions_path, 'r') as file:
                region_data = file.read()
            self.regions = {region.strip(): True for region in region_data.splitlines() if region.strip()}
            print("Loaded regions:", self.regions)
        except FileNotFoundError:
            print(f"Region file not found at {regions_path}. Ensure the file exists.")
        except Exception as e:
            print(f"An error occurred while loading regions: {e}")

    def set_regions(self, only_solve):
        """Initialize and configure active regions."""
        if only_solve:
            if only_solve in self.regions:
                self.nsolve = {only_solve: True}
            else:
                print(f"Region '{only_solve}' is not in the loaded regions. Ensure the region is valid.")
        else:
            self.nsolve = {region: True for region in self.regions}

        # Set regions as active
        self.regions = {region: True for region in self.nsolve}

    def include_data(self):
        """Handle the include_data phase."""
        print("[RegionModule] Handling 'include_data' phase.")
        # Placeholder for additional data loading logic
        print("Loading additional region-related data (if required).")

    def compute_data(self):
        """Handle the compute_data phase."""
        print("[RegionModule] Handling 'compute_data' phase.")
        # Placeholder for additional computations related to regions
        print("Computing data for regions (if required).")

    def report(self):
        """Handle the report phase."""
        print("[RegionModule] Handling 'report' phase.")
        # Add logic for reporting data
        print("Reporting regional computations and results.")

    def handle_phase(self, phase, datapath='./data/', only_solve=None):
        self.phase = phase
        self.datapath = datapath
        self.only_solve = only_solve

        if self.phase == 'conf':
            print("[RegionModule] Handling 'conf' phase.")
            self.load_config(datapath)
        elif self.phase == 'sets':
            print("[RegionModule] Handling 'sets' phase.")
            self.load_regions(datapath)
            self.set_regions(only_solve)
        elif self.phase == 'include_data':
            print("[RegionModule] Handling 'include_data' phase.")
            self.include_data()
        elif self.phase == 'compute_data':
            print("[RegionModule] Handling 'compute_data' phase.")
            self.compute_data()
        elif self.phase == 'declare_vars':
            print("[RegionModule] Handling 'declare_vars' phase.")
            # Add logic for declare_vars
        elif self.phase == 'compute_vars':
            print("[RegionModule] Handling 'compute_vars' phase.")
            # Add logic for compute_vars
        elif self.phase == 'report':
            print("[RegionModule] Handling 'report' phase.")
            self.report()
        elif self.phase == 'gdx_items':
            print("[RegionModule] Handling 'gdx_items' phase.")
            print("Regions to be processed:", list(self.regions.keys()))
        else:
            raise ValueError(f"Unknown phase: {self.phase}. Must be 'conf', 'sets', 'include_data', 'compute_data', 'declare_vars', 'compute_vars', 'report', or 'gdx_items'.")


# Example usage
if __name__ == "__main__":
    # Example for 'conf' phase
    handle_phase(phase='conf', datapath='./data/')

    # Example for 'sets' phase with specific region
    handle_phase(phase='sets', datapath='./data/', only_solve='Region1')

    # Example for 'include_data' phase
    handle_phase(phase='include_data', datapath='./data/')

    # Example for 'compute_data' phase
    handle_phase(phase='compute_data', datapath='./data/')

    # Example for 'report' phase
    handle_phase(phase='report', datapath='./data/')

    # Example for 'gdx_items' phase
    handle_phase(phase='gdx_items', datapath='./data/')
