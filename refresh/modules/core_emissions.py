# EMISSIONS MODULE
# Where Regions emissions are determined.

# =========================================================================
#   ///////////////////////       SETTING      ///////////////////////
# =========================================================================

# CONF
# Definition of the global flags and settings specific to the module
t_min_miu = 9  # MIU linear-transition time horizon from 1 to maximum upperbound
t_max_miu = 38  # MIU maximum reachable upperbound
max_miuup = 1.2  # MIU maximum reachable upperbound

# Carbon-intensity transition curve types
sig_trns_type = 'sigmoid_Ls'

# Time of full-convergence to dice-ref carbon-intensity curve
sig_trns_end = 38

# SSP-n hypothesis on dice-reference curve for carbon-intensity
sig_dice_ref_curve = 'discounted'

# =========================================================================
#   ///////////////////////       SETS        ///////////////////////
# =========================================================================

ere = {
    "co2",
    "co2ffi",  # Fossil-fuel and Industry CO2
    "nip",     # Net import of permits
    "sav",     # Saved permits
    "kghg",    # Kyoto greenhouse gases
    "ch4",
    "n2o",
    "sf6"
}

map_e = {
    ("co2", "co2ffi")
}

ghg = {"co2", "ch4", "n2o"}
oghg = {"ch4", "n2o"}

# =========================================================================
#   ///////////////////////       DATA        ///////////////////////
# =========================================================================

# Hardcoded parameters
cumeind0 = 400     # Starting cumulative emissions from industry [GtC]
cumetree0 = 100    # Starting cumulative emissions from land use deforestation [GtC]
fosslim = 6000     # Maximum cumulative extraction fossil fuels [GtC]
miu0 = 0           # Initial emissions control rate
min_miu = 1.00     # Upper bound for control rate MIU at t_min_miu
max_miu = max_miuup
min_miuoghg = 0.7
max_miuoghg = 1

# Conversion coefficients
CtoCO2 = 44 / 12
CO2toC = 12 / 44

# =========================================================================
#   ///////////////////////      VARIABLES      ///////////////////////
# =========================================================================

# Variables with initial levels
EIND = lambda t, n, sigma, ykali, MIU: sigma[t][n] * ykali[t][n] * (1 - MIU[t][n])
E = lambda t, n, EIND, ELAND, E_NEG=None: EIND[t][n] + ELAND[t][n] - (E_NEG[t][n] if E_NEG else 0)
CCAEIND = lambda t, CCAEIND_prev, EIND_sum: CCAEIND_prev + (EIND_sum * CO2toC)
CUMETREE = cumetree0
MIU = lambda t, n: 0

# Upper bounds for MIU
def compute_MIU_upper_bounds(t_values, t_min_miu, t_max_miu, min_miu, max_miu):
    MIU_bounds = {}
    for t in t_values:
        if t < t_min_miu:
            MIU_bounds[t] = min_miu
        elif t_min_miu <= t <= t_max_miu:
            MIU_bounds[t] = min_miu + (max_miu - min_miu) * (t - t_min_miu) / (t_max_miu - t_min_miu)
        else:
            MIU_bounds[t] = max_miu
    return MIU_bounds

# =========================================================================
#   ///////////////////////     EQUATIONS      ///////////////////////
# =========================================================================

# Industrial emissions
def eq_eind(t, n, sigma, ykali, MIU):
    return EIND(t, n, sigma, ykali, MIU)

# All emissions
def eq_e(t, n, EIND, ELAND, E_NEG=None):
    return E(t, n, EIND, ELAND, E_NEG)

# Cumulative industrial emissions in Carbon
def eq_ccaeind(t, CCAEIND_prev, EIND_sum):
    return CCAEIND(t, CCAEIND_prev, EIND_sum)

# =========================================================================
# Add further logic for looping and computing if necessary
# =========================================================================

# Usage Example
t_values = range(1, 50)  # Example time steps
MIU_bounds = compute_MIU_upper_bounds(t_values, t_min_miu, t_max_miu, min_miu, max_miu)
print(MIU_bounds)
