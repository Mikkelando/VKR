import numpy as np

class ExogenousTATMClimateModel:
    def __init__(self, tatm_inc_tstep=0.05, force2015=2.4634, tatm2010=0.80, tcorr=0.3291984):
        # Initialization of model parameters
        self.tatm_inc_tstep = tatm_inc_tstep
        self.force2015 = force2015
        self.tatm2010 = tatm2010
        self.tcorr = tcorr
        
        # Model constants (parameters)
        self.fex0 = 0.5
        self.fex1 = 1.0
        self.t2xco2 = 3.1
        self.fco22x = 3.6813
        self.c10 = 0.098
        self.c1beta = 0.01243
        self.c1 = 0.1005
        self.c3 = 0.088
        self.c4 = 0.025

        # Initialize variables
        self.temp_tatm_exogen = None
        self.forcoth = None
        self.fcorr = None
        self.force0ev = None

    def load_exogenous_data(self, results_for_fixed_tatm):
        """
        Load exogenous temperature data from external source (e.g., GDX or external file).
        """
        # For the sake of the example, assuming results_for_fixed_tatm is a dictionary
        # with key 'TATM.l' containing the temperature data
        self.temp_tatm_exogen = results_for_fixed_tatm['TATM.l']

    def compute_data(self):
        """
        Compute the temperature changes and forcing data.
        """
        # If no external data is provided, use a simplified trajectory for TATM
        if self.temp_tatm_exogen is None:
            self.temp_tatm_exogen = [self.tatm2010 + self.tatm_inc_tstep * (t - 1) for t in range(1, 101)]
        
        # OGHG forcing exogenous (DICE-like)
        self.forcoth = np.zeros(100)
        for t in range(1, 18):
            self.forcoth[t-1] = self.fex0 + (1/17) * (self.fex1 - self.fex0) * (t - 1)
        for t in range(18, 101):
            self.forcoth[t-1] = self.fex1

        # Transient TSC correction (Speed of Adjustment Parameter)
        self.c1 = self.c10 + self.c1beta * (self.t2xco2 - 2.9)

        # Compute starting forcing level
        self.force0ev = ((self.fco22x / self.t2xco2) * self.tatm2010) + ((self.tatm2010 - self.tatm2010) / self.c1) + (self.c3 * (self.tatm2010 - 0))
        
        # Compute correction factor for radiative forcing
        self.fcorr = 0.6 * (self.force2015 - self.force0ev)

    def compute_vars(self):
        """
        Compute initial values for forcing and temperature.
        """
        # Initial values for forcing and TATM
        FORC = np.zeros(100)
        TATM = np.zeros(100)

        FORC[0] = self.force2015
        TATM[0] = -np.inf  # Lower bound for TATM
        TATM[1] = np.inf   # Upper bound for TATM

        return FORC, TATM

    def eqs(self, TATM, TOCEAN):
        """
        Set up equations for temperature (TATM) and ocean (TOCEAN).
        """
        # Atmosphere
        eq_tatm = TATM - self.temp_tatm_exogen

        # Ocean
        eq_tocean = TOCEAN + self.c4 * (TATM - TOCEAN)

        # Forcing
        eq_forc = (self.fco22x / self.t2xco2) * TATM + ((TATM[1] - TATM[0]) / self.c1) + (self.c3 * (TATM - TOCEAN)) + self.fcorr

        return eq_tatm, eq_tocean, eq_forc

    def report(self):
        """
        Report GDX items or final results.
        """
        # In this case, return the computed temperature changes
        return self.temp_tatm_exogen


if __name__ == "__main__":
    # Example of using the model
    model = ExogenousTATMClimateModel()
    model.load_exogenous_data({'TATM.l': np.linspace(0.8, 2.5, 100)})  # Example external data
    model.compute_data()
    FORC, TATM = model.compute_vars()
    eq_tatm, eq_tocean, eq_forc = model.eqs(TATM, np.zeros(100))

    # Report results
    print(model.report())
