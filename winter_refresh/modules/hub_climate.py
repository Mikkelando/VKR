class ClimateModule:
    def __init__(self, policy=None):
        self.climate = 'witchco2'  # Default climate model
        self.default_climate = 'witchco2'
        
        if policy == 'simulation_tatm_exogen':
            self.climate = 'tatm_exogen'
        elif policy == 'simulation_climate_regional_exogen':
            self.climate = 'tatm_exogen'
        
        # Parameters (Initial values from WITCH bau)
        self.tatm0 = 1.12  # Initial Atmospheric Temperature change [degree C from 1900]
        self.tocean0 = 0.109427  # Initial Lower Stratum Temperature change [degree C from 1900]
        
        # Variables (to be computed later)
        self.FORC = {}  # Increase in Radiative Forcing [W/m2 from 1900]
        self.TATM = {}  # Increase Temperature of Atmosphere [degrees C from 1900]
        self.TOCEAN = {}  # Increase Temperature of Lower Oceans [degrees C from 1900]
        
        # Starting levels
        self.TATM_levels = {'t': self.tatm0}
        self.TOCEAN_levels = {'t': self.tocean0}
        
        # Setup initial levels and ranges
        self.setup_initial_conditions()

    def setup_initial_conditions(self):
        # Temperature ranges
        self.TATM_UP = 40
        self.TATM_LO = -10
        self.TATM_fx = self.tatm0  # Initial condition for TATM
        
        self.TOCEAN_UP = 20
        self.TOCEAN_LO = -1
        self.TOCEAN_FX = self.tocean0  # Initial condition for TOCEAN

    def compute_forc(self, t):
        # Example: Radiative Forcing equation (can be expanded with real calculations)
        self.FORC[t] = 1.0  # Placeholder for actual equation

    def compute_tatm(self, t):
        # Example: Temperature equation for Atmosphere (can be expanded with real calculations)
        self.TATM[t] = self.TATM_fx + 0.1 * t  # Placeholder for actual equation

    def compute_tocean(self, t):
        # Example: Temperature equation for Lower Oceans (can be expanded with real calculations)
        self.TOCEAN[t] = self.TOCEAN_FX + 0.05 * t  # Placeholder for actual equation

    def report(self):
        # Reporting climate parameters and variables
        return {
            'tatm0': self.tatm0,
            'tocean0': self.tocean0,
            'FORC': self.FORC,
            'TATM': self.TATM,
            'TOCEAN': self.TOCEAN
        }

# -------------------------------------------------
# Глобальная функция handle_phase
# -------------------------------------------------
def handle_phase(phase, *args, **kwargs):
    """
    Handle different phases of the hub_climate module.
    """
    climate_module = ClimateModule(policy=kwargs.get('policy'))

    if phase == "conf":
        print("[hub_climate] Handling 'conf' phase")
        # Initialize or reset configurations if necessary

    elif phase == "sets":
        print("[hub_climate] Handling 'sets' phase")
        print(f"Climate model selected: {climate_module.climate}")

    elif phase == "include_data":
        print("[hub_climate] Handling 'include_data' phase")
        print(f"Initial TATM: {climate_module.tatm0}, Initial TOCEAN: {climate_module.tocean0}")

    elif phase == "compute_data":
        print("[hub_climate] Handling 'compute_data' phase")
        # Example: compute forcing and temperatures for a specific time step
        time_step = kwargs.get('time_step', 1)
        climate_module.compute_forc(time_step)
        climate_module.compute_tatm(time_step)
        climate_module.compute_tocean(time_step)
        print(f"Computed FORC, TATM, and TOCEAN for time step {time_step}")

    elif phase == "declare_vars":
        print("[hub_climate] Handling 'declare_vars' phase")
        # Declare variables or ranges

    elif phase == "compute_vars":
        print("[hub_climate] Handling 'compute_vars' phase")
        # Compute variables based on logic (example given below)
        time_step = kwargs.get('time_step', 1)
        climate_module.compute_forc(time_step)
        print(f"Computed FORC for time step {time_step}: {climate_module.FORC[time_step]}")

    elif phase == "report":
        print("[hub_climate] Handling 'report' phase")
        report = climate_module.report()
        print("Climate Report:", report)

    else:
        print(f"[hub_climate] Unknown phase: {phase}")


# ========================== MAIN EXECUTION ==========================
if __name__ == "__main__":
    handle_phase("conf", policy="simulation_tatm_exogen")
    handle_phase("sets")
    handle_phase("include_data")
    handle_phase("compute_data", time_step=1)
    handle_phase("declare_vars")
    handle_phase("compute_vars", time_step=1)
    handle_phase("report")
