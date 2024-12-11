class RegionModule:
    def __init__(self, phase, datapath, only_solve=None):
        self.phase = phase
        self.datapath = datapath
        self.only_solve = only_solve
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

    def load_config(self):
        """Load configuration data from the specified path."""
        config_path = f"{self.datapath}regions.conf"
        with open(config_path, 'r') as file:
            config_data = file.read()
        print("Loaded configuration:", config_data)

    def load_regions(self):
        """Load region data from the specified path."""
        regions_path = f"{self.datapath}regions.inc"
        with open(regions_path, 'r') as file:
            region_data = file.read()
        print("Loaded regions:", region_data)

    def set_regions(self):
        """Initialize and configure active regions."""
        if self.only_solve:
            self.nsolve = {self.only_solve: True}
        else:
            self.nsolve = {region: True for region in self.regions}

        # No limits for the moment
        self.regions = {region: True for region in self.nsolve}

    def handle_phase(self):
        """Handle different phases of the module."""
        if self.phase == 'conf':
            self.load_config()
        elif self.phase == 'sets':
            self.load_regions()
            self.set_regions()
        elif self.phase == 'gdx_items':
            print("Regions to be processed:", list(self.regions.keys()))
        else:
            raise ValueError(f"Unknown phase: {self.phase}")


# Example usage
if __name__ == "__main__":
    # Initialize module
    module = RegionModule(phase='sets', datapath='./data/', only_solve='Region1')

    # Handle the specified phase
    module.handle_phase()
