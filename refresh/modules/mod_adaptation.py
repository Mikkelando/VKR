#-------------------------------------------------------------------------------
# Long-run Damages from Climate Change
# - Economic impacts
# - Adaptation
#-------------------------------------------------------------------------------

# Define global variables based on phase
phase = 'conf'  # Set phase based on context

# Set adaptation efficiency based on baseline
baseline = 'ssp2'  # Example baseline, modify as needed
adap_efficiency = 'ssp2'
if baseline == 'ssp1':
    adap_efficiency = 'ssp1_ssp5'
elif baseline == 'ssp3':
    adap_efficiency = 'ssp3'
elif baseline == 'ssp5':
    adap_efficiency = 'ssp1_ssp5'

# Define sets for adaptation sectors
iq = ['ada', 'cap', 'act', 'gcap']  # Nodes representing economic values
g = ['prada', 'rada', 'scap']  # Adaptation sectors

# Initialize parameters for adaptation depreciation
dk_ada = {'prada': 0.1, 'rada': 1, 'scap': 0.03}

# Load data for adaptation efficiency
ces_ada = {'eff': {n: 1 for n in range(5)}, 'tfpada': {n: 1 for n in range(5)}}  # Simplified example
owa = {'act': {n: 1 for n in range(5)}, 'cap': {n: 1 for n in range(5)}, 'actc': {n: 1 for n in range(5)}}
k_h0 = {n: 1 for n in range(5)}  # Example data
k_edu0 = {n: 1 for n in range(5)}  # Example data

# Set adaptation efficiency based on adaptation efficiency type
if adap_efficiency == 'ssp2':
    for n in range(5):
        ces_ada['eff'][n] = 1
elif adap_efficiency == 'ssp1_ssp5':
    for n in range(5):
        ces_ada['eff'][n] = 1.25
elif adap_efficiency == 'ssp3':
    for n in range(5):
        ces_ada['eff'][n] = 0.75

# Initialize variables
K_ADA = {'prada': {}, 'rada': {}, 'scap': {}}  # Capital in different sectors
I_ADA = {'prada': {}, 'rada': {}, 'scap': {}}  # Investments in different sectors
Q_ADA = {iq_: {n: 1e-5 for n in range(5)} for iq_ in iq}  # Adaptation quantities

# Define variable bounds
for iq_ in iq:
    for n in range(5):
        Q_ADA[iq_][n] = {'lo': 1e-8, 'up': 1e3, 'l': 1e-5}

# Set initial values for K_ADA and I_ADA
for sector in g:
    for n in range(5):
        K_ADA[sector][n] = {'lo': 1e-8, 'up': 1e3, 'l': 1e-8}
        I_ADA[sector][n] = {'lo': 1e-8, 'up': 1e3, 'l': 1e-8}

# Initial values for K_ADA in the first period
tfirst = 0  # Example, modify as needed
for sector in ['prada', 'rada', 'scap']:
    for n in range(5):
        K_ADA[sector][n] = {'fx': 1e-5}

# Compute equations for adaptation and investment
def eqq_ada(t, n):
    # Equation for adaptation quantity
    result = ces_ada['tfpada'][n] * (
        owa['act'][n] * Q_ADA['act'][t][n] ** ces_ada['ada'][n] +
        owa['cap'][n] * Q_ADA['cap'][t][n] ** ces_ada['ada'][n]
    ) ** (1 / ces_ada['ada'][n])
    return result

def eqq_act(t, n):
    # Equation for adaptation quantity in the activity sector
    result = ces_ada['eff'][n] * owa['actc'][n] * (
        owa['rada'][n] * I_ADA['rada'][t][n] ** ces_ada['act'][n] +
        owa['prada'][n] * K_ADA['prada'][t][n] ** ces_ada['act'][n]
    ) ** (1 / ces_ada['act'][n])
    return result

def eqq_cap(t, n):
    # Equation for adaptation quantity in the capital sector
    result = (
        owa['gcap'][n] * Q_ADA['gcap'][t][n] ** ces_ada['cap'][n] +
        owa['scap'][n] * K_ADA['scap'][t][n] ** ces_ada['cap'][n]
    ) ** (1 / ces_ada['cap'][n])
    return result

def eqq_gcap(t, n):
    # Equation for gross capital
    result = ((k_h0[n] + k_edu0[n]) / 2) * tfp(t, n)
    return result

# Placeholder function for total factor productivity (TFP)
def tfp(t, n):
    return 1  # Simplified for example


if __name__ == "__main__":
    # Reporting phase
    # Collect the variables for reporting
    gdx_items = {
        'ces_ada': ces_ada,
        'k_edu0': k_edu0,
        'k_h0': k_h0,
        'owa': owa,
        'K_ADA': K_ADA,
        'I_ADA': I_ADA,
        'Q_ADA': Q_ADA
    }

    # Final report output
    print(gdx_items)
