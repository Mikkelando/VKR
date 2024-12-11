
##HUGE RE-WORK to MASTER-CLASS !!


# Define phase and modules dynamically
phase = "some_phase"  # This would be provided as input or set dynamically

# Simulating module imports
def import_module(module_name):
    try:
        exec(f"import {module_name}")
        print(f"Module {module_name} imported successfully.")
    except ImportError as e:
        print(f"Failed to import {module_name}: {str(e)}")

# Core blocks
import_module('core_time')  # Core block to align correctly time periods
import_module('core_regions')  # Regions settings and exogenous data imports
import_module('core_economy')  # Core block for economy
import_module('core_emissions')  # Core block for emissions
import_module('core_welfare')  # Core block for welfare

# Cooperation setup based on a variable
cooperation = "some_cooperation"  # This would be dynamically set
import_module(f'cooperation_{cooperation}')  # Cooperation setup

# Solve settings
import_module('core_algorithm')  # Solve settings

# Module for MAC curves, abatement cost
import_module('mod_macc')  # MAC curves, abatement cost

# Other specialized modules
import_module('mod_land_use')  # Land-use HUB
import_module('hub_climate')  # Climate HUB
import_module('mod_climate_regional')  # Regional climate module
import_module('hub_impact')  # Climate Impact HUB

# Policy
import_module('core_policy')  # All policy options
pol_ndc = True  # Example condition, set dynamically
if pol_ndc:
    import_module('pol_ndc')  # NDC policy module

# Optional modules, conditionally imported
mod_adaptation = True  # Example condition, set dynamically
if mod_adaptation:
    import_module('mod_adaptation')  # Adaptation Module

mod_government = False  # Example condition, set dynamically
if mod_government:
    import_module('mod_government')  # Government Module

mod_labour = False  # Example condition, set dynamically
if mod_labour:
    import_module('mod_labour')  # Labour Module

mod_inequality = True  # Example condition, set dynamically
if mod_inequality:
    import_module('mod_inequality')  # Inequality Module

mod_srm = False  # Example condition, set dynamically
if mod_srm:
    import_module('mod_srm')  # Solar Radiation Management Module

mod_slr = True  # Example condition, set dynamically
if mod_slr:
    import_module('mod_slr')  # Sea level rise Module

mod_natural_capital = False  # Example condition, set dynamically
if mod_natural_capital:
    import_module('mod_natural_capital')  # Nature Capital Green Module

mod_emission_pulse = True  # Example condition, set dynamically
if mod_emission_pulse:
    import_module('mod_emission_pulse')  # Emission Pulse for SCC computation

mod_dac = False  # Example condition, set dynamically
if mod_dac:
    import_module('mod_emi_stor')  # Emission storage module
    import_module('mod_dac')  # Negative emissions module
