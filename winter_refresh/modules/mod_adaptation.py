class AdaptationModule:
    def __init__(self):
        # Global flags and settings
        self.baseline = 'ssp2'  # Default baseline
        self.adap_efficiency = self.set_adap_efficiency(self.baseline)
        
        # Define sets for adaptation sectors
        self.iq = ['ada', 'cap', 'act', 'gcap']
        self.g = ['prada', 'rada', 'scap']
        
        # Parameters
        self.dk_ada = {'prada': 0.1, 'rada': 1, 'scap': 0.03}
        self.ces_ada = {'eff': {n: 1 for n in range(5)}, 'tfpada': {n: 1 for n in range(5)}}
        self.owa = {'act': {n: 1 for n in range(5)}, 'cap': {n: 1 for n in range(5)}, 'actc': {n: 1 for n in range(5)}}
        self.k_h0 = {n: 1 for n in range(5)}
        self.k_edu0 = {n: 1 for n in range(5)}
        
        # Variables
        self.K_ADA = {sector: {n: 1e-5 for n in range(5)} for sector in self.g}
        self.I_ADA = {sector: {n: 1e-5 for n in range(5)} for sector in self.g}
        self.Q_ADA = {iq_: {n: 1e-5 for n in range(5)} for iq_ in self.iq}

    def set_adap_efficiency(self, baseline):
        if baseline == 'ssp1':
            return 'ssp1_ssp5'
        elif baseline == 'ssp3':
            return 'ssp3'
        elif baseline == 'ssp5':
            return 'ssp1_ssp5'
        else:
            return 'ssp2'

    def conf(self):
        """ Handle the configuration phase """
        print("Configuration Phase")
        self.adap_efficiency = self.set_adap_efficiency(self.baseline)

    def sets(self):
        """ Handle the sets phase """
        print("Sets Phase")
        self.iq = ['ada', 'cap', 'act', 'gcap']
        self.g = ['prada', 'rada', 'scap']

    def include_data(self):
        """ Handle the include data phase """
        print("Include Data Phase")
        # Example of setting initial values
        for sector in self.g:
            for n in range(5):
                self.K_ADA[sector][n] = 1e-5
                self.I_ADA[sector][n] = 1e-5

    def compute_vars(self):
        """ Handle the compute variables phase """
        print("Compute Variables Phase")
        # Placeholder logic for computing variables
        for iq_ in self.iq:
            for n in range(5):
                self.Q_ADA[iq_][n] = self.ces_ada['eff'][n] * 1e-5

    def gdx_items(self):
        """ Handle the GDX items phase """
        print("GDX Items Phase")
        return {
            'ces_ada': self.ces_ada,
            'owa': self.owa,
            'K_ADA': self.K_ADA,
            'I_ADA': self.I_ADA,
            'Q_ADA': self.Q_ADA
        }


# Глобальная функция handle_phase
def handle_phase(phase, **kwargs):
    """
    Глобальная функция для управления фазами модуля адаптации.
    """
    module = AdaptationModule()

    if phase == "conf":
        print("[mod_adaptation] Configuring...")
        module.conf()

    elif phase == "sets":
        print("[mod_adaptation] Defining sets...")
        module.sets()

    elif phase == "include_data":
        print("[mod_adaptation] Including data...")
        module.include_data()

    elif phase == "compute_vars":
        print("[mod_adaptation] Computing variables...")
        module.compute_vars()

    elif phase == "gdx_items":
        print("[mod_adaptation] Listing GDX items...")
        gdx_items = module.gdx_items()
        print("GDX Items:", gdx_items)

    else:
        print(f"[mod_adaptation] Unknown phase: {phase}")


if __name__ == "__main__":
    # Пример использования
    handle_phase("conf")
    handle_phase("sets")
    handle_phase("include_data")
    handle_phase("compute_vars")
    handle_phase("gdx_items")
