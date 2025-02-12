"""
modules.py

Equivalent of the GAMS script 'modules.gms'.

Handles the inclusion and calling of various Python modules based on 'phase' and optional flags
(e.g., cooperation type, policy modules, etc.).
"""

from modules.core_time import handle_phase as core_time_handle
from modules.core_regions import handle_phase as core_regions_handle
from modules.core_economy import handle_phase as core_economy_handle
from modules.core_emissions import handle_phase as core_emissions_handle
from modules.core_welfare import handle_phase as core_welfare_handle
from modules.core_algorithm import handle_phase as core_algorithm_handle
from modules.cooperation_coop import handle_phase as coop_coop_handle
from modules.cooperation_noncoop import handle_phase as coop_noncoop_handle
from modules.mod_macc import handle_phase as mod_macc_handle
from modules.mod_land_use import handle_phase as mod_land_use_handle
from modules.hub_climate import handle_phase as hub_climate_handle
from modules.mod_climate_regional import handle_phase as mod_climate_regional_handle
from modules.hub_impact import handle_phase as hub_impact_handle
from modules.core_policy import handle_phase as core_policy_handle
from modules.pol_ndc import handle_phase as pol_ndc_handle
from modules.mod_adaptation import handle_phase as mod_adaptation_handle

def handle_modules(phase, arg2=None, cooperation=None, baseline=None, t_vals=None, n_vals=None):
    """
    Mimics the logic of modules.gms by calling Python equivalents.
    :param phase: The 'phase' in GAMS (e.g. 'conf', 'sets', etc.)
    :param arg2: Additional argument (equivalent to %2).
    :param cooperation: The cooperation mode (e.g. 'coop', 'noncoop').
    :param baseline: The baseline scenario (e.g. 'ssp2').
    :param t_vals: Time intervals for compute_data phase.
    :param n_vals: Regions for compute_data phase.
    """
    # 1) Core modules
    core_time_handle(phase)
    core_regions_handle(phase, arg2)
    core_economy_handle(phase)
    core_emissions_handle(phase)
    core_welfare_handle(phase, t_vals=t_vals, n_vals=n_vals)

    # 2) Cooperation module
    if cooperation == "coop":
        coop_coop_handle(phase)
    elif cooperation == "noncoop":
        coop_noncoop_handle(phase)

    # 3) Core algorithm (solving settings)
    core_algorithm_handle(phase)

    # 4) Additional modules
    mod_macc_handle(phase)
    mod_land_use_handle(phase)
    hub_climate_handle(phase)
    mod_climate_regional_handle(phase)
    hub_impact_handle(phase)
    core_policy_handle(phase)

    # 5) Policy NDC
    if baseline == "pol_ndc":
        pol_ndc_handle(phase)

    # 6) Optional modules
    mod_adaptation_handle(phase)

    print(f"Completed handling all modules for phase='{phase}', arg2='{arg2}'.")
