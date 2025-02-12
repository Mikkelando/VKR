import numpy as np

# Parameters
kw_DT = 0.00641
kw_DT_lag = 0.00345
kw_TDT = -0.00105
kw_TDT_lag = -0.000718
kw_T = -0.00675

# Example data (replace with actual values from your model)
TEMP_REGION_DAM = np.array([[0.1, 0.2], [0.15, 0.25], [0.2, 0.3]])  # Temperature region damage
tlen = np.array([1, 1, 1])  # Time lengths (example)

# Variables initialization
BIMPACT = np.zeros_like(TEMP_REGION_DAM)  # Impact coefficients
KOMEGA = np.ones_like(TEMP_REGION_DAM)  # Initial KOMEGA values

# For simplicity, let's assume a range of time periods (e.g., 3 time steps) and regions (e.g., 2 regions)
T = len(TEMP_REGION_DAM)  # Time steps
N = TEMP_REGION_DAM.shape[1]  # Number of regions

# Function to calculate BHM impact
def compute_bimpact(TEMP_REGION_DAM, tlen, kw_DT, kw_DT_lag, kw_TDT, kw_TDT_lag):
    BIMPACT = np.zeros_like(TEMP_REGION_DAM)
    for t in range(2, T):  # Starting from the 2nd time step (excluding the first)
        for n in range(N):  # Loop over regions
            BIMPACT[t, n] = (kw_DT + kw_DT_lag) * (TEMP_REGION_DAM[t, n] - TEMP_REGION_DAM[t - 1, n]) + \
                            (kw_TDT + kw_TDT_lag) * (TEMP_REGION_DAM[t, n] - TEMP_REGION_DAM[t - 1, n]) / tlen[t] * \
                            (2 * (TEMP_REGION_DAM[t, n] - TEMP_REGION_DAM[t - 1, n]) + 5 * TEMP_REGION_DAM[t - 1, n])
    return BIMPACT

# Function to calculate Omega (impact over time)
def compute_omega(BIMPACT, KOMEGA, omega_eq='simple'):
    OMEGA = np.zeros_like(BIMPACT)
    for t in range(1, T - 1):  # Looping over time steps (excluding first and last)
        for n in range(N):
            if omega_eq == 'full':
                # Full Omega formula (adjusted for the model)
                # Example of basegrowthcap, tfp, pop, K, etc., would need to be passed in actual use
                OMEGA[t + 1, n] = (1 + OMEGA[t, n]) * (1 + BIMPACT[t, n]) - 1  # Placeholder for full formula
            elif omega_eq == 'simple':
                # Simple Omega formula
                OMEGA[t + 1, n] = 1 / (BIMPACT[t + 1, n] + 1 / (1 + OMEGA[t, n])) - 1
    return OMEGA

if __name__ == "__main__":
    # Calculate BIMPACt and OMEGA
    BIMPACT = compute_bimpact(TEMP_REGION_DAM, tlen, kw_DT, kw_DT_lag, kw_TDT, kw_TDT_lag)
    OMEGA = compute_omega(BIMPACT, KOMEGA, omega_eq='simple')

    # Reporting of results
    print(f"BIMPACT (Damage Coefficients):\n{BIMPACT}")
    print(f"OMEGA (Impact over time):\n{OMEGA}")
