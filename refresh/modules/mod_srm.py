# Import necessary modules
import numpy as np
import random

# Global variables and constants
geoeng_start = 2035  # Period when SRM becomes available
maxsrm = 2  # Maximum amount of SRM per region (in MtS)
damage_geoeng = True  # Activate damages from SRM
impsrm_exponent = 2  # Exponent of the damage function
damage_geoeng_amount = 0.03  # Damage amount
geoeng_forcing = -1.75  # Forcing per TgS
geoeng_residence_in_atm = 2  # Atmospheric residence time in years

# Initialize dictionaries and parameters
SRM = {}
SRM_COST = {}
W_SRM = {}
srm_available = {}
wsrm = {}
n_active = {}

# Initialize global parameters
def set_srm_available(t, n, geoeng_start, geoeng_end=2250, only_region=None, multiple_regions=None, srm_ub=None):
    # Initialize SRM availability based on the conditions
    if t >= geoeng_start and t <= geoeng_end:
        if only_region and n != only_region:
            srm_available[(t, n)] = False
        elif multiple_regions and n not in n_active:
            srm_available[(t, n)] = False
        else:
            srm_available[(t, n)] = True
    else:
        srm_available[(t, n)] = False

# Initialize SRM costs
def set_srm_cost(t, n):
    SRM_COST[(t, n)] = (geoeng_forcing / geoeng_residence_in_atm) / 1000 * (SRM[(t, n)] ** impsrm_exponent)

# Initialize the SRM
def initialize_srm(t, n, randomize=False):
    if randomize:
        srm_init = random.uniform(0, 0.5)
        SRM[(t, n)] = srm_init
    else:
        SRM[(t, n)] = 0

# Main loop for SRM logic
def geoengineering_loop(years, regions):
    for t in years:
        for n in regions:
            # Activate SRM availability for the given region and year
            set_srm_available(t, n, geoeng_start)

            # Initialize SRM values
            if t >= geoeng_start:
                initialize_srm(t, n, randomize=True)

            # Calculate SRM costs
            set_srm_cost(t, n)

            # Calculate W_SRM (World SRM injection values)
            wsrm[t] = sum(SRM[(t, n)] for n in regions)

            # Additional computations as needed
            W_SRM[(t, n)] = wsrm[t]
            print(f"Year {t}, Region {n}: SRM = {SRM[(t, n)]}, SRM_COST = {SRM_COST[(t, n)]}, W_SRM = {W_SRM[(t, n)]}")


if __name__ == "__main__":
    # Example usage
    years = range(2035, 2051)  # Simulate for 2035-2050
    regions = ['region_1', 'region_2', 'region_3']

    geoengineering_loop(years, regions)
