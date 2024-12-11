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


if __name__ == "__main__":

    # Example of using the class
    climate_module = ClimateModule(policy='simulation_tatm_exogen')

    # Compute variables for a specific time
    time_step = 1
    climate_module.compute_forc(time_step)
    climate_module.compute_tatm(time_step)
    climate_module.compute_tocean(time_step)

    # Report the results
    results = climate_module.report()
    print(results)
