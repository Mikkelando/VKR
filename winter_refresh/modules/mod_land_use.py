import numpy as np
import pandas as pd

# Constants and parameters
CtoCO2 = 3.664  # conversion factor from carbon to CO2
deland = 0.115  # Decline rate of land emissions (per period)

# Set of years for land use calculations
years = np.arange(1850, 2301)

# Sample region and emission data (use your actual data here)
regions = ['region1', 'region2', 'region3']  # Example regions
historical_data = pd.DataFrame({
    'yearlu': np.tile(years, len(regions)),
    'region': np.repeat(regions, len(years)),
    'q_emi_valid_oscar': np.random.rand(len(years) * len(regions)),  # Random emission data
})

# Compute LU-Baseline
def compute_baseline(historical_data, years):
    eland0 = {}
    for region in regions:
        avg_emissions = historical_data[
            (historical_data['region'] == region) & 
            (historical_data['yearlu'] >= 2005) & 
            (historical_data['yearlu'] < 2015)
        ].groupby('yearlu')['q_emi_valid_oscar'].mean().values
        eland0[region] = CtoCO2 * np.sum(avg_emissions) / 10  # Average over the last 10 years
    return eland0

eland0 = compute_baseline(historical_data, years)

# Compute BAU Emissions
def compute_eland_bau(eland0, deland, years, policy="bau"):
    eland_bau = {}
    for policy_type in ['uniform', 'differentiated']:
        eland_bau[policy_type] = {}
        for t in years:
            for region in regions:
                if policy == "bau":
                    eland_bau[policy_type][(t, region)] = eland0[region] * (1 - deland) ** (t - 1)
                elif policy == "bau_impact":
                    eland_bau[policy_type][(t, region)] = eland0[region] * (1 - deland) ** (t - 1)
                else:
                    eland_bau[policy_type][(t, region)] = min(eland0[region] * (1 - deland) ** (t - 1), eland0[region])
    return eland_bau

eland_bau = compute_eland_bau(eland0, deland, years, policy="bau")

# Compute cumulative emissions
def compute_cumulative_emissions(eland_bau, years):
    cumeland_bau = {}
    global_cumeland_bau = {'uniform': {}, 'differentiated': {}}
    
    for policy_type in ['uniform', 'differentiated']:
        cumeland_bau[policy_type] = {1: 0}  # starting value is 0
        for t in years[:-1]:
            for region in regions:
                cumeland_bau[policy_type][t + 1] = cumeland_bau[policy_type].get(t, 0) + eland_bau[policy_type].get((t, region), 0)
                
        global_cumeland_bau[policy_type] = sum(cumeland_bau[policy_type].values())
    
    return cumeland_bau, global_cumeland_bau

cumeland_bau, global_cumeland_bau = compute_cumulative_emissions(eland_bau, years)

# Variables for emissions based on policy
def compute_land_use_emissions(eland_bau, policy="bau"):
    ELAND = {}
    for policy_type in ['uniform', 'differentiated']:
        for t in years:
            for region in regions:
                if policy == 'bau' or policy == 'bau_impact':
                    ELAND[(t, region)] = eland_bau['uniform'][(t, region)]
                else:
                    ELAND[(t, region)] = eland_bau['differentiated'][(t, region)]
    return ELAND

# -------------------------------------------------
# Глобальная функция handle_phase
# -------------------------------------------------
def handle_phase(phase, *args, **kwargs):
    """
    Обрабатывает различные фазы модуля mod_land_use.
    """
    if phase == "conf":
        print("[mod_land_use] Handling 'conf' phase")
        # Логика конфигурации

    elif phase == "sets":
        print("[mod_land_use] Handling 'sets' phase")
        print(f"Regions: {regions}")

    elif phase == "include_data":
        print("[mod_land_use] Handling 'include_data' phase")
        print("Baseline land emissions (eland0):", eland0)

    elif phase == "compute_data":
        print("[mod_land_use] Handling 'compute_data' phase")
        print("Computing BAU emissions and cumulative emissions")
        global eland_bau, cumeland_bau, global_cumeland_bau
        eland_bau = compute_eland_bau(eland0, deland, years, policy="bau")
        cumeland_bau, global_cumeland_bau = compute_cumulative_emissions(eland_bau, years)

    elif phase == "declare_vars":
        print("[mod_land_use] Handling 'declare_vars' phase")
        # Объявление переменных

    elif phase == "compute_vars":
        print("[mod_land_use] Handling 'compute_vars' phase")
        ELAND = compute_land_use_emissions(eland_bau, policy="bau")
        print(f"Land use emissions (ELAND): {list(ELAND.items())[:5]}")  # Печатаем первые 5 записей для проверки

    elif phase == "report":
        print("[mod_land_use] Handling 'report' phase")
        report_results(eland0, deland, compute_land_use_emissions(eland_bau))

    else:
        print(f"[mod_land_use] Unknown phase: {phase}")

# Reporting / Output results
def report_results(eland0, deland, ELAND):
    print("Land-use emissions (ELAND):")
    for (t, region), value in list(ELAND.items())[:10]:  # Печатаем первые 10 записей для проверки
        print(f"Year: {t}, Region: {region}, Emission: {value:.2f} GtCO2/year")
    
    print("\nBaseline emissions (eland0):")
    for region, value in eland0.items():
        print(f"Region: {region}, Baseline Emission: {value:.2f} GtCO2/year")
    
    print(f"\nDecline rate (deland): {deland}")

# ========================== MAIN EXECUTION ==========================
if __name__ == "__main__":
    handle_phase("conf")
    handle_phase("sets")
    handle_phase("include_data")
    handle_phase("compute_data")
    handle_phase("declare_vars")
    handle_phase("compute_vars")
    handle_phase("report")
