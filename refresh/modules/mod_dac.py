
##HUGE RE-WORK !!
### CREATE GLOBAL SETTER MASTER-CLASS



# MODULE TEMPLATE
# Short description

# ========================================================================
# ///////////////////////       SETTING      /////////////////////////////
# ========================================================================

# activate with --dac=1

## CONF
# ___________________________________________________________
# Definition of the global flags and settings specific to the module

if phase == 'conf':
    # By default, DAC are the only source of negative emissions if activated
    global noneg

    if baseline == 'ssp1':
        global costdac, residual_emissions
        costdac = 'low'
        residual_emissions = 'low'
    elif baseline == 'ssp2':
        global costdac, residual_emissions
        costdac = 'best'
        residual_emissions = 'medium'
    elif baseline == 'ssp3':
        global costdac, residual_emissions
        costdac = 'high'
        residual_emissions = 'high'
    elif baseline == 'ssp4':
        global costdac, residual_emissions
        costdac = 'best'
        residual_emissions = 'low'
    elif baseline == 'ssp5':
        global costdac, residual_emissions
        costdac = 'low'
        residual_emissions = 'high'

    global burden_share
    burden_share = 'geo'

    global max_cdr
    max_cdr = 40

## SETS
# ___________________________________________________________
# Declare sets and add new elements as needed

elif phase == 'sets':
    pass  # Implement any set declarations here

## INCLUDE DATA
# ___________________________________________________________
# Declare and include exogenous parameters

elif phase == 'include_data':
    twh2ej = 0.0036

    c2co2 = 44 / 12

    dac_tot0 = 453 * 1e-3  # Initial total costs of DAC [T$/GtonCO2]
    dac_totfloor = 100 * 1e-3  # Floor total costs [T$/GtonCO2]

    dac_totcost = {}

    capex = 0.4  # Fraction of LCOD due to investments
    lifetime = 20  # DAC lifetime in years

    dac_delta_en = 1 - exp(1 / (-lifetime + (0.01 / 2) * lifetime ** 2))  # DAC lifetime calculation

    capstorreg = {}
    totcapstor = 0

    mkt_growth_rate_dac = {}

    mkt_growth_free_dac = {}
    mkt_growth_free_dac[t, n] = 0.001 / 5

    dac_learn = {}

    wcum_dac = {}
    for t in year_range:
        if year(t) <= 2015:
            wcum_dac[t] = 0.001 * 5


## COMPUTE DATA
# ___________________________________________________________
# Compute parameters that depend on the data loaded in the previous phase

elif phase == 'compute_data':
    dac_tot0 = 453 * 1e-3  # Source: RFF expert elicitation (Soheil Shayegh, 2020)

    if mkt_growth_dac == 'high':
        for t, n in mkt_growth_rate_dac:
            mkt_growth_rate_dac[t, n] = 0.1
    elif mkt_growth_dac == 'low':
        for t, n in mkt_growth_rate_dac:
            mkt_growth_rate_dac[t, n] = 0.03
    else:
        for t, n in mkt_growth_rate_dac:
            mkt_growth_rate_dac[t, n] = 0.06

    if costdac == 'high':
        for t, n in dac_learn:
            dac_learn[t, n] = 0.06  # Source: RFF expert elicitation (Soheil Shayegh, 2020)
    elif costdac == 'low':
        for t, n in dac_learn:
            dac_learn[t, n] = 0.22  # Source: RFF expert elicitation (Soheil Shayegh, 2020)
    else:
        for t, n in dac_learn:
            dac_learn[t, n] = 0.136  # Source: RFF expert elicitation (Soheil Shayegh, 2020)

    dac_totfloor = 100 * 1e-3  # Long term floor cost
    for t, n in dac_totcost:
        dac_totcost[t, n] = dac_tot0

    for n in capstorreg:
        capstorreg[n] = sum(ccs_stor(ccs_stor_cap_max(n))) / c2co2
    totcapstor = sum(capstorreg.values())


## DECLARE VARIABLES
# ___________________________________________________________
# Declare new variables for the module

elif phase == 'declare_vars':
    E_NEG = {}  # Installed capacity of DAC [GtCO2/yr]
    I_CDR = {}  # Yearly investment of DAC [T$/yr]
    COST_CDR = {}  # Yearly total cost of DAC [T$/yr]
    REV_CDR = {}  # Total revenues of DAC industry [T$/yr]
    GOVSUR = {}  # Government surplus [Trill 2005 USD / year]

    # VARIABLES STARTING LEVELS
    E_NEG_l = {}  # Starting levels for E_NEG
    GOVSUR_l = {}  # Starting levels for GOVSUR

    for t, n in E_NEG_l:
        E_NEG_l[t, n] = 0
    for t, n in GOVSUR_l:
        GOVSUR_l[t, n] = 0


## COMPUTE VARIABLES
# ___________________________________________________________
# Fix starting points and bounds

elif phase == 'compute_vars':
    E_NEG_lo = {}
    COST_CDR_up = {}
    REV_CDR_up = {}
    I_CDR_up = {}

    for t, n in E_NEG_lo:
        E_NEG_lo[t, n] = 1e-15

    for t, n in COST_CDR_up:
        COST_CDR_up[t, n] = 0.25 * ykali[t, n]

    for t, n in REV_CDR_up:
        REV_CDR_up[t, n] = 0.5 * ykali[t, n]

    for t, n in I_CDR_up:
        I_CDR_up[t, n] = 30 / c2co2

    if burden_share == "geo":
        for t, n in E_NEG_up:
            E_NEG_up[t, n] = capstorreg[n] / 5697 * max_cdr

    elif burden_share == "epc":
        for t, n in E_NEG_up:
            E_NEG_up[t, n] = pop[2, n] / sum(pop[2, nn] for nn in n) * totcapstor / 5697 * max_cdr

    elif burden_share == "hist_resp":
        # Load historical data
        q_emi_valid_primap = load_gdx('data_%n%/data_historical_values')

        for t, n in E_NEG_up:
            E_NEG_up[t, n] = sum(q_emi_valid_primap['co2ffi', yearlu, n] for yearlu in yearlu) / \
                             sum(q_emi_valid_primap['co2ffi', yearlu, nn] for yearlu, nn in zip(yearlu, nn)) * \
                             totcapstor / 5697 * max_cdr

    # Avoid errors in the climate module
    I_CDR_up[t, n] = 0  # To avoid errors after 2100

    # Fix investments before 2020
    for t, n in E_NEG_up:
        E_NEG_up[t, n] = 1e-3 * capstorreg[n] / totcapstor

    I_CDR_fx = {}  # Fixed investments at tfirst
    E_NEG_fx = {}  # Fixed DAC capacities at tfirst

    for tfirst, n in I_CDR_fx:
        I_CDR_fx[tfirst, n] = 0
    for tfirst, n in E_NEG_fx:
        E_NEG_fx[tfirst, n] = 1e-8


# ========================================================================
# ///////////////////////     OPTIMIZATION    /////////////////////////////
# ========================================================================

## EQUATION LIST
# ___________________________________________________________
# List of equations
eq_depr_e_neg = 'eq_depr_e_neg'
eq_cost_cdr = 'eq_cost_cdr'
eq_emi_stor_dac = 'eq_emi_stor_dac'
eq_mkt_growth_dac = 'eq_mkt_growth_dac'
eq_rev_cdr = 'eq_rev_cdr'
eq_govbal = 'eq_govbal'
eq_netzero = 'eq_netzero'

## EQUATIONS
# ___________________________________________________________
# Implement equations

elif phase == 'eqs':
    pass  # Add equations here

## BEFORE SOLVE
# ___________________________________________________________
# Update parameters right before solving the model

elif phase == 'before_solve':
    pass  # Add logic to execute before solving the model
