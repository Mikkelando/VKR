import numpy as np
import pandas as pd

# Define Constants
MAX_TEMP_REGION_DAM = 30  # Maximum temperature observed in regions' past time series [°C]
DELTA_TEMPCAP = 1e-4  # Tolerance for min/max NLP smoothing

# Simulating loaded climate data and coefficients (to be replaced by actual data loading methods)
climate_region_coef = {
    'alpha_temp': np.random.random(10),  # Example coefficients for alpha
    'beta_temp': np.random.random(10),   # Example coefficients for beta
    'base_temp': np.random.random(10)    # Example base temperature for each region
}

pop = np.random.random(10)  # Population distribution
TATM = np.random.random(20)  # Global mean temperature (extended mock data)

# ========================== FUNCTIONS ==========================

def compute_past_temperature(tincpast, tatm_valid, temp_valid_yearlu, tstep=1):
    tatm_valid_updated = np.sum(
        np.array([temp_valid_yearlu[t] for t in tincpast]), axis=0
    ) / (len(tincpast) * tstep)
    return tatm_valid_updated

def compute_temp_region(t, n, climate_region_coef, TATM):
    """
    Compute the local temperature for each region using downscaling equations.
    Ensure index `t` is within bounds.
    """
    if t >= len(TATM):
        raise IndexError(f"Index t={t} is out of bounds for TATM with length {len(TATM)}")
    return climate_region_coef['alpha_temp'][n] + climate_region_coef['beta_temp'][n] * TATM[t]

def cap_temperature(TEMP_REGION, t, n, max_temp_region_dam, delta_tempcap):
    return min(TEMP_REGION[t, n], max_temp_region_dam)

def compute_temp_region_dam(TEMP_REGION, t, n, max_temp_region_dam, delta_tempcap):
    return (TEMP_REGION[t, n] + max_temp_region_dam - 
            np.sqrt(np.square(TEMP_REGION[t, n] - max_temp_region_dam) + np.square(delta_tempcap))) / 2

def compute_deltas(temp_region_dam, temp_region_base):
    return temp_region_dam - temp_region_base

# ========================== HANDLE PHASE ==========================

def handle_phase(phase, *args, **kwargs):
    if phase == "compute_data":
        years = kwargs.get('years', np.arange(1980, 2011))
        regions = kwargs.get('regions', np.arange(10))

        TEMP_REGION = np.zeros((len(years), len(regions)))
        TEMP_REGION_DAM = np.zeros((len(years), len(regions)))

        for t_index, t in enumerate(years):
            for n in regions:
                if t_index >= len(TATM):
                    print(f"Skipping year={t}, region={n}: Index t={t_index} out of bounds for TATM with length {len(TATM)}")
                    TEMP_REGION[t_index, n] = None
                    TEMP_REGION_DAM[t_index, n] = None
                    continue
                
                TEMP_REGION[t_index, n] = compute_temp_region(t_index, n, climate_region_coef, TATM)
                TEMP_REGION_DAM[t_index, n] = compute_temp_region_dam(TEMP_REGION, t_index, n, MAX_TEMP_REGION_DAM, DELTA_TEMPCAP)

        print("Computed regional temperatures and damages.")



# ========================== MAIN EXECUTION ==========================

if __name__ == "__main__":
    handle_phase("conf")
    handle_phase("sets")
    handle_phase("include_data")
    TEMP_REGION, TEMP_REGION_DAM = handle_phase("compute_data", years=np.arange(1980, 2011), regions=np.arange(10))
    handle_phase("declare_vars")
    handle_phase("compute_vars")
    handle_phase("report")
