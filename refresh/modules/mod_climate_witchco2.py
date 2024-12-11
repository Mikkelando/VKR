import numpy as np

# Constants (from the provided data)
CO2toC = 0.27  # Conversion factor for CO2 to carbon
tstep = 1  # Time step (could be yearly)
ghg = ['co2', 'methane', 'nitrous_oxide']  # Example greenhouse gases
time_steps = 100  # Example number of time steps
t_values = np.arange(1, time_steps + 1)

# Parameters (values loaded from the external data)
fex0 = 0.5  # 2015 forcings of non-CO2 GHG [Wm-2]
fex1 = 1.0  # 2100 forcings of non-CO2 GHG [Wm-2]
emi_gwp = {
    'co2': 1.0,
    'methane': 25.0,
    'nitrous_oxide': 298.0
}
tempc = {
    'sigma1': 0.01,
    'lambda': 0.02,
    'sigma2': 0.015,
    'heat_ocean': 0.02
}

# Initialize arrays for world emissions and other variables
W_EMI = {ghg_type: np.zeros(time_steps) for ghg_type in ghg}
WCUM_EMI = {ghg_type: np.zeros((3, time_steps)) for ghg_type in ghg}  # Assuming 3 climate layers
RF = {ghg_type: np.zeros(time_steps) for ghg_type in ghg}
RFoth = np.zeros(time_steps)
FORC = np.zeros(time_steps)
TATM = np.zeros(time_steps)
TOCEAN = np.zeros(time_steps)

# Functions
def linear_interpolation(fex0, fex1, t):
    """Linear interpolation for exogenous forcing."""
    if t < 18:
        return fex0 + (1 / 17) * (fex1 - fex0) * (t - 1)
    else:
        return fex1

def radiative_forcing(wcum_emi, rfc_alpha, rfc_beta):
    """Calculate radiative forcing."""
    return rfc_alpha * (np.log(wcum_emi) - np.log(rfc_beta))

def update_world_emissions(emi_gwp, co2_to_c, emissions, wemi2qemi):
    """Update world emissions based on carbon and GWP conversion."""
    for ghg_type in ghg:
        W_EMI[ghg_type] = (np.sum(emissions) * co2_to_c) / wemi2qemi[ghg_type]
    return W_EMI


if __name__ == "__main__":
    # Initialize coefficients for OGHG forcing
    oghg_coeff = {
        'intercept': 0.1,
        'slope': 0.3
    }

    # Main simulation loop (over time steps)
    for t in range(1, time_steps):
        # Exogenous forcing for other GHGs
        forcoth = linear_interpolation(fex0, fex1, t)
        RFoth[t] = oghg_coeff['intercept'] + oghg_coeff['slope'] * RF['co2'][t]

        # Update emissions
        W_EMI = update_world_emissions(emi_gwp, CO2toC, W_EMI, emi_gwp)

        # Update WCUM_EMI (accumulation of GHGs in climate layers)
        for m in range(3):
            WCUM_EMI['co2'][m, t] = np.sum(WCUM_EMI['co2'][:, t - 1]) * 0.9 + (tstep * W_EMI['co2'][t])  # Example transfer

        # Calculate CO2 radiative forcing
        RF['co2'][t] = radiative_forcing(WCUM_EMI['co2'][0, t], rfc_alpha=0.5, rfc_beta=2.0)

        # Total radiative forcing
        FORC[t] = RF['co2'][t] + RFoth[t]

        # Global temperature increase from pre-industrial levels
        TATM[t] = TATM[t - 1] + tempc['sigma1'] * (FORC[t] - tempc['lambda'] * TATM[t] - tempc['sigma2'] * (TATM[t] - TOCEAN[t]))

        # Ocean temperature
        TOCEAN[t] = TOCEAN[t - 1] + tempc['heat_ocean'] * (TATM[t] - TOCEAN[t])

    # Results (reporting phase)
    print("Final temperature increase (TATM):", TATM[-1])
    print("Final ocean temperature (TOCEAN):", TOCEAN[-1])
    print("Final radiative forcing (RF):", RF['co2'][-1])
