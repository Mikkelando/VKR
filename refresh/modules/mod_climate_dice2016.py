import numpy as np

class ClimateModel:
    def __init__(self):
        # Initial Conditions (from the DICE2016 model)
        self.mat0 = 851  # GtC (Initial Concentration in Atmosphere 2015)
        self.mu0 = 460   # GtC (Initial Concentration in Upper Strata 2015)
        self.ml0 = 1740  # GtC (Initial Concentration in Lower Strata 2015)
        self.mateq = 588  # GtC (Equilibrium concentration in atmosphere)
        self.mueq = 360   # GtC (Equilibrium concentration in upper strata)
        self.mleq = 1720  # GtC (Equilibrium concentration in lower strata)
        self.matpre = 588.0  # GtC (Concentration in Atmosphere at pre-industrial level)

        # Flow Parameters
        self.b12 = 0.088
        self.b23 = 0.007

        # Climate model parameters
        self.t2xco2 = 3.1  # Degree C per doubling of CO2
        self.fex0 = 0.5    # 2015 forcings of non-CO2 GHG
        self.fex1 = 1.0    # 2100 forcings of non-CO2 GHG
        self.fco22x = 3.6813  # Forcings of equilibrium CO2 doubling (Wm-2)
        self.c10 = 0.098
        self.c1beta = 0.01243
        self.c1 = 0.1005
        self.c3 = 0.088
        self.c4 = 0.025

        # Forcing parameters for other GHG (Exogenous)
        self.forcoth = None

        # Time-dependent variables (can be modified in the future)
        self.timestep = 1  # Placeholder for time step

    def update_flow_parameters(self):
        self.b11 = 1 - self.b12
        self.b21 = self.b12 * self.mateq / self.mueq
        self.b22 = 1 - self.b21 - self.b23
        self.b32 = self.b23 * self.mueq / self.mleq
        self.b33 = 1 - self.b32

    def compute_forcing(self, t):
        """
        Exogenous forcing for other greenhouse gases.
        Linear interpolation from fex0 to fex1 from t1 to t17,
        then constant after t17.
        """
        if t < 18:
            self.forcoth = self.fex0 + (1/17) * (self.fex1 - self.fex0) * (t - 1)
        else:
            self.forcoth = self.fex1

    def compute_transient_tsc(self):
        """
        Transient TSC Correction based on temperature sensitivity.
        """
        self.c1 = self.c10 + self.c1beta * (self.t2xco2 - 2.9)

    def initialize_variables(self):
        # Initialize carbon concentrations at the start of the simulation
        self.MAT = np.zeros(100)  # Placeholder for time steps
        self.MU = np.zeros(100)
        self.ML = np.zeros(100)
        
        # Set initial values
        self.MAT[0] = self.mat0
        self.MU[0] = self.mu0
        self.ML[0] = self.ml0

    def carbon_cycle(self, t):
        """
        Update the carbon concentrations based on the carbon cycle equations.
        """
        self.MAT[t+1] = self.MAT[t] * self.b11 + self.MU[t] * self.b21
        self.MU[t+1] = self.MAT[t] * self.b12 + self.MU[t] * self.b22 + self.ML[t] * self.b32
        self.ML[t+1] = self.MU[t] * self.b23 + self.ML[t] * self.b33

    def forcing_equation(self, t):
        """
        Forcing equation based on CO2 concentration and other forcings.
        """
        return self.fco22x * np.log(self.MAT[t] / self.matpre) / np.log(2) + self.forcoth

    def temperature_equations(self, t):
        """
        Temperature equations for atmosphere and ocean.
        """
        TATM = np.zeros(100)
        TOCEAN = np.zeros(100)
        
        TATM[t+1] = TATM[t] + self.c1 * ((self.forcing_equation(t) - (self.fco22x / self.t2xco2) * TATM[t]) - self.c3 * (TATM[t] - TOCEAN[t]))
        TOCEAN[t+1] = TOCEAN[t] + self.c4 * (TATM[t] - TOCEAN[t])
        
        return TATM, TOCEAN

    def run_simulation(self, max_years):
        """
        Runs the full simulation for a given number of years.
        """
        for t in range(1, max_years):
            self.compute_forcing(t)
            self.compute_transient_tsc()
            self.carbon_cycle(t)
            TATM, TOCEAN = self.temperature_equations(t)
            print(f"Year {t}: TATM = {TATM[t]}, TOCEAN = {TOCEAN[t]}")


if __name__=="__main__":
    #    Usage 
    climate_model = ClimateModel()
    climate_model.update_flow_parameters()
    climate_model.initialize_variables()
    climate_model.run_simulation(100)  # Simulate for 100 years
