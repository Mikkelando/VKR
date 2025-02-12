import numpy as np
import pandas as pd

# =============================================================================
# SETTINGS
# =============================================================================

# Configurations
bhm_spec = 'sr'  # 'sr', 'lr', 'srdiff', 'lrdiff'
cutoff = 'median'  # 'median', 'avg'
omega_eq = 'simple'  # 'simple', 'full'
dam_endo = ''  # Endogenous or post-processed damage
damage_cap = True
omegabnd = ''  # 'default' or '_UNBOUNDED'

# =============================================================================
# PARAMETERS
# =============================================================================

# Short run and long run coefficients (from the data or fixed values)
bhm_SR_T = 0.0127184
bhm_SR_T2 = -0.0004871
bhm_LR_T = -0.0037497
bhm_LR_T2 = -0.0000955

# Short-run differentiated coefficients (rich and poor)
bhm_SRdiff_rich_T = 0.0088951
bhm_SRdiff_rich_T2 = -0.0003155
bhm_SRdiff_poor_T = 0.0254342
bhm_SRdiff_poor_T2 = -0.000772

# Long-run differentiated coefficients (rich and poor)
bhm_LRdiff_rich_T = -0.0026918
bhm_LRdiff_rich_T2 = -0.000022
bhm_LRdiff_poor_T = -0.0186
bhm_LRdiff_poor_T2 = 0.0001513

# Simulated data for GDP per capita and population (to be replaced with actual data)
n = 100  # number of countries/regions
t = 10  # number of years

# Simulated GDP per capita and population data (as examples)
ykali = np.random.rand(t, n) * 10000  # GDP per capita
pop = np.random.randint(1000000, 10000000, (t, n))  # Population
temp_region = np.random.rand(t, n) * 2  # Temperature change

# Calculate world average and median GDP per capita
ykalicap_median = np.median(ykali, axis=1)  # Median GDP per capita
ykalicap_worldavg = np.mean(ykali, axis=1)  # World average GDP per capita

# Rich/poor cutoff evaluation based on median or average
if cutoff == 'median':
    rich_poor_cutoff = ykalicap_median
else:
    rich_poor_cutoff = ykalicap_worldavg

# =============================================================================
# COMPUTE IMPACT COEFFICIENTS
# =============================================================================

def compute_bhm_impact():
    beta_bhm = np.zeros((2, n, t))  # T and T^2 coefficients

    # Short-run specification
    if bhm_spec == 'sr':
        beta_bhm[0, :, :] = bhm_SR_T
        beta_bhm[1, :, :] = bhm_SR_T2
    
    # Long-run specification
    elif bhm_spec == 'lr':
        beta_bhm[0, :, :] = bhm_LR_T
        beta_bhm[1, :, :] = bhm_LR_T2

    # Short-run differentiated by income
    elif bhm_spec == 'srdiff':
        for i in range(n):
            if ykali[:, i] > rich_poor_cutoff:  # Rich
                beta_bhm[0, i, :] = bhm_SRdiff_rich_T
                beta_bhm[1, i, :] = bhm_SRdiff_rich_T2
            else:  # Poor
                beta_bhm[0, i, :] = bhm_SRdiff_poor_T
                beta_bhm[1, i, :] = bhm_SRdiff_poor_T2

    # Long-run differentiated by income
    elif bhm_spec == 'lrdiff':
        for i in range(n):
            if ykali[:, i] > rich_poor_cutoff:  # Rich
                beta_bhm[0, i, :] = bhm_LRdiff_rich_T
                beta_bhm[1, i, :] = bhm_LRdiff_rich_T2
            else:  # Poor
                beta_bhm[0, i, :] = bhm_LRdiff_poor_T
                beta_bhm[1, i, :] = bhm_LRdiff_poor_T2
    
    return beta_bhm

beta_bhm = compute_bhm_impact()

# =============================================================================
# COMPUTE IMPACTS AND OMEGA
# =============================================================================

def compute_omega():
    omega = np.zeros((t, n))  # Omega factor for each country and time
    KOMEGA = np.ones((t, n))  # Capital-Omega factor
    
    for year in range(t-1):
        # Calculate Omega using the full equation
        if omega_eq == 'full':
            omega[year+1, :] = ((1 + omega[year, :]) * 
                                (1 + 0.02) *  # TFP factor (example)
                                (pop[year+1, :] / pop[year, :]) ** 0.1)  # Population factor (example)
        
        # Simple Omega equation
        else:
            omega[year+1, :] = (1 + omega[year, :]) / (1 + beta_bhm[0, :, year]) - 1
    
    return omega, KOMEGA

omega, KOMEGA = compute_omega()

# =============================================================================
# FINAL IMPACT CALCULATIONS
# =============================================================================

def compute_bimpact():
    BIMPACT = np.zeros((t, n))  # Impact coefficient
    
    for year in range(1, t):
        BIMPACT[year, :] = (beta_bhm[0, :, year] * temp_region[year, :] - 
                            beta_bhm[1, :, year] * temp_region[year, :]**2)
    
    return BIMPACT


if __name__ == "__main__":

    BIMPACT = compute_bimpact()

    # =============================================================================
    # REPORTING
    # =============================================================================

    # The following steps would simulate the results and prepare reports.
    # Here we just show an example output of the BIMPACT and OMEGA for review.

    print("BIMPACT (Impact Coefficients):")
    print(BIMPACT)

    print("\nOMEGA (Omega Factors):")
    print(omega)
