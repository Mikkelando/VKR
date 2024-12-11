
#### RE-WORK !!


import numpy as np
import pandas as pd

# Define Constants
MAX_TEMP_REGION_DAM = 30  # Maximum temperature observed in regions' past time series [°C]
DELTA_TEMPCAP = 1e-4  # Tolerance for min/max nlp smoothing

# Simulating loaded climate data and coefficients (to be replaced by actual data loading methods)
climate_region_coef = {
    'alpha_temp': np.random.random(10),  # Example coefficients for alpha
    'beta_temp': np.random.random(10),   # Example coefficients for beta
    'base_temp': np.random.random(10)    # Example base temperature for each region
}

pop = np.random.random(10)  # Population distribution
TATM = np.random.random(10)  # Global mean temperature (mock data)

# Historical temperatures for past data (mocked)
tatm_valid = np.random.random(10)  # Historical temperature anomalies

# Temp data for regions (mocked)
temp_region_valid = np.random.random((10, 10))  # 10 regions, 10 years

# Downscaling coefficients (mocked)
climate_region_coef_downscale = {
    'alpha_temp': np.random.random(10),
    'beta_temp': np.random.random(10)
}

# Functions to simulate phase logic
def compute_past_temperature(tincpast, tatm_valid, temp_valid_yearlu, tstep=1):
    # Calculate average 5-year temperature based on the HadCRUT data
    tatm_valid_updated = np.sum(
        np.array([temp_valid_yearlu[t] for t in tincpast]), axis=0
    ) / (len(tincpast) * tstep)
    return tatm_valid_updated

def compute_temp_region(t, n, climate_region_coef, TATM):
    # Calculate the local temperature for each region using the downscaling equation
    return climate_region_coef['alpha_temp'][n] + climate_region_coef['beta_temp'][n] * TATM[t]

def cap_temperature(TEMP_REGION, t, n, max_temp_region_dam, delta_tempcap):
    # Apply Burke's conservative approach for temperature capping for damages evaluation
    return min(TEMP_REGION[t, n], max_temp_region_dam)

def compute_temp_region_dam(TEMP_REGION, t, n, max_temp_region_dam, delta_tempcap):
    # Compute temperature used for damages evaluation
    return (TEMP_REGION[t, n] + max_temp_region_dam - np.sqrt(np.square(TEMP_REGION[t, n] - max_temp_region_dam) + np.square(delta_tempcap))) / 2

def compute_deltas(temp_region_dam, temp_region_base):
    # Calculate the difference between current and base temperatures
    return temp_region_dam - temp_region_base


if __name__ == "__main__":
    # Mock data for years, regions, etc.
    years = np.arange(1980, 2011)
    regions = np.arange(10)

    # Example data structures for TEMP_REGION and TEMP_REGION_DAM
    TEMP_REGION = np.random.random((len(years), len(regions)))  # Local avg temperatures for each year and region
    TEMP_REGION_DAM = np.random.random((len(years), len(regions)))  # Damaged evaluated temperatures

    # Example: Compute average temperature over the years
    tatm_valid_updated = compute_past_temperature(years, tatm_valid, temp_region_valid)

    # Example: Calculate regional temperatures
    for t in years:
        for n in regions:
            TEMP_REGION[t, n] = compute_temp_region(t, n, climate_region_coef, TATM)

            # Applying conservative capping for damages evaluation
            TEMP_REGION_DAM[t, n] = compute_temp_region_dam(TEMP_REGION, t, n, MAX_TEMP_REGION_DAM, DELTA_TEMPCAP)

    # Example: Calculate deltas between current and base temperatures
    temp_region_base = climate_region_coef['base_temp']
    deltatemp = compute_deltas(TEMP_REGION_DAM, temp_region_base)

    # Reporting and final calculations
    temp_mean_world_weighted = np.sum(pop * climate_region_coef['alpha_temp']) / np.sum(pop) + \
                            (np.sum(pop * climate_region_coef['beta_temp']) / np.sum(pop)) * np.mean(TATM)

    # Output the results
    print("Regional Temperature Deltas (Damages):")
    print(deltatemp)

    print("\nWorld Weighted Temperature Mean:")
    print(temp_mean_world_weighted)

