import numpy as np

# Constants (global settings)
macc = 'ed'  # Marginal Abatement Cost Curve formula (use 'ed' as default)
mxdataref = 'ssp2marker'  # Data reference for the correction multiplier

# Backstop data (DICE2016 as default)
pback = 550  # Cost of backstop (2015 USD per tCO2)
gback = 0.025  # Initial cost decline for backstop
expcost2 = 2.8  # Exponent of control cost function
tstart_pbtransition = 7  # Starting transition time to backstop
tend_pbtransition = 23  # Full convergence to backstop time
klogistic = 0.25  # Parameter influencing logistic transition speed

# MACC Shape fitting model (polynomial 1-4 as default)
maccfit = "poly14fit"

# Define sectors
sectors = ['Total_CO2', 'Total_CH4', 'Total_N2O']

# MX alternative data references
mxdatarefs = ['ssp2marker', 'advance', 'ssp2markerXT', 'advanceXT']

# Data loading placeholders (would typically load data from files)
# In this case, loading is simulated as placeholder values
MXkali = {ref: np.random.random() for ref in mxdatarefs}

# CO2 MAC-Curves fitting parameters (simulated data for coefficients)
macc_co2 = {
    'Total_CO2': {
        'a': np.random.random(10),  # Example coefficients for 'a'
        'b': np.random.random(10)   # Example coefficients for 'b'
    }
}

# OGHG MAC-Curves fitting parameters (simulated data for coefficients)
macc_oghg = {
    'Total_CO2': {
        'a': np.random.random(10),  # Example coefficients for 'a'
        'b': np.random.random(10)   # Example coefficients for 'b'
    }
}

# Initialize backstop price over time (pbacktime function)
def pbacktime(t):
    return pback * (1 - gback) ** (t - 1)

# Adjusted cost for Backstop
def cost1(t, n, sigma_fn):
    return pbacktime(t) * sigma_fn(t, n) / expcost2 / 1000

# Logistic function for transition
def alpha(t):
    x0 = tstart_pbtransition + (tend_pbtransition - tstart_pbtransition) / 2
    return 1 / (1 + np.exp(-klogistic * (t - x0)))

# Calculate multiplier for the backstop curve (MXpback)
def MXpback(t, n):
    ax = macc_co2['Total_CO2']['a'][n]
    bx = macc_co2['Total_CO2']['b'][n]
    return pbacktime(t) / (ax + bx * (1 ** 4))

# Transition to backstop multiplier (MXstart and MXend)
def transition_multiplier(t, n):
    MXstart = MXkali[mxdataref]
    MXend = MXpback(t, n)
    MXdiff = max(MXstart - MXend, 0)
    return MXstart - alpha(t) * MXdiff

# Compute emissions reductions cost (ABATECOST equation)
def compute_abatecost(t, n, MIU_fn, emi_bau_co2_fn):
    ax = macc_co2['Total_CO2']['a'][n]
    bx = macc_co2['Total_CO2']['b'][n]
    MIU = MIU_fn(t, n)
    emi_bau = emi_bau_co2_fn(t, n)
    return transition_multiplier(t, n) * ((ax * MIU ** 2 / 2) + (bx * MIU ** 5 / 5)) * emi_bau / 1000

# Example of how to use these functions to compute costs
def MIU(t, n):
    return 1  # Placeholder for MIU function

def emi_bau_co2(t, n):
    return np.random.random()  # Placeholder for baseline emission function



if __name__ == "__main__":
    # Calculate the abatement cost for given time (t) and scenario (n)
    t = 10
    n = 5
    abate_cost = compute_abatecost(t, n, MIU, emi_bau_co2)
    print(f"Abatement Cost at time {t}, scenario {n}: {abate_cost}")