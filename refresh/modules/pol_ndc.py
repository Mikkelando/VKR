class ModuleTemplate:
    def __init__(self):
        # Global flags and settings
        self.ndcs_extr = "linear"  # Default to "linear"
        self.nameout = "baseline_ndc_linear_cooperation_extrlinear"
        self.output_filename = f"results_{self.nameout}"
        self.ctax_start = 2035

        # Set variables
        self.miu_fixed_levels = {}
        self.miu_ndcs_2030 = {}
        self.cprice_hotel = {}
        self.CPRICE = {}
        self.MIU = {}
        self.mx = {}
        self.ax_co2 = {}
        self.bx_co2 = {}

    def conf(self):
        """ Handle the configuration phase """
        print("Configuration Phase")
        # Global flags and settings
        self.ndcs_extr = "linear"
        self.nameout = "baseline_ndc_linear_cooperation_extrlinear"
        self.output_filename = f"results_{self.nameout}"
        self.ctax_start = 2035

    def sets(self):
        """ Handle the sets phase """
        print("Sets Phase")
        # Declare sets (for this example, we use `tmiufix`)
        self.tmiufix = {1, 2, 3, 4}

    def include_data(self):
        """ Handle the include data phase """
        print("Include Data Phase")
        # Example: parameter cprice_hotel(t,n)
        # Initialize cprice_hotel as zero for each combination of t, n
        self.cprice_hotel = {(t, n): 0 for t in range(1, 6) for n in range(1, 6)}

    def compute_vars(self):
        """ Handle the compute variables phase """
        print("Compute Vars Phase")
        # Compute variables and set bounds
        if self.policy == "bau":
            for t in range(1, 6):
                for n in range(1, 6):
                    if t not in self.tmiufix:
                        self.MIU[t, n] = 0  # Undo MIU fix
                        self.MIU[t, n] = max_miu  # Max MIU value
                    self.MIU[t, n] = self.miu_fixed_levels.get((t, n), 0)  # Fix MIU for certain periods

                    # Recompute cprice values
                    self.CPRICE[t, n] = self.mx.get((t, n), 1) * (
                        self.ax_co2.get((t, n), 0) * self.MIU[t, n] + 
                        self.bx_co2.get((t, n), 0) * self.MIU[t, n] ** 4
                    )

    def before_solve(self):
        """ Handle the before solve phase """
        print("Before Solve Phase")
        if self.ndcs_extr == "const":
            for t in range(1, 6):
                for n in range(1, 6):
                    if t > 2030:
                        self.CPRICE[t, n] = min(self.CPRICE.get((4, n), 0), 
                                                 self.mx.get((t, n), 1) * (
                                                     self.ax_co2.get((t, n), 0) * self.MIU[t, n] +
                                                     self.bx_co2.get((t, n), 0) * self.MIU[t, n] ** 4))

        elif self.ndcs_extr == "linear":
            for t in range(1, 6):
                for n in range(1, 6):
                    if t > 2030 and self.CPRICE.get((2, n), 0) != 0:
                        self.CPRICE[t, n] = min(
                            self.CPRICE.get((4, n), 0) * (1 + (self.CPRICE.get((4, n), 0) - self.CPRICE.get((2, n), 0)) / 
                                                         (self.CPRICE.get((4, n), 0) * 2) * (t - 2030)),
                            self.mx.get((t, n), 1) * (
                                self.ax_co2.get((t, n), 0) * self.MIU[t, n] + 
                                self.bx_co2.get((t, n), 0) * self.MIU[t, n] ** 4
                            )
                        )

        elif self.ndcs_extr == "hotelling":
            for t in range(1, 6):
                for n in range(1, 6):
                    self.cprice_hotel[(4, n)] = self.CPRICE.get((4, n), 0)
                    for tt in range(1, t+1):
                        if t > 2030:
                            self.cprice_hotel[(t, n)] = self.cprice_hotel.get((tt, n), 0) * (
                                1 + prstp + elasmu * (ykali(t, n) - ykali(tt, n)) / (tstep * ykali(tt, n))
                            ) ** tstep

                        self.CPRICE[t, n] = min(self.cprice_hotel.get((t, n), 0), 
                                                 self.mx.get((t, n), 1) * (
                                                     self.ax_co2.get((t, n), 0) * self.MIU[t, n] +
                                                     self.bx_co2.get((t, n), 0) * self.MIU[t, n] ** 4
                                                 ))

        # Recompute ctax corrected to avoid inconsistencies with NDCs
        for t in range(1, 6):
            for n in range(1, 6):
                self.ctax_corrected = max(self.CPRICE[t, n], min(self.ctax.get((t, n), 0) * 1000,
                                                                self.mx.get((t, n), 1) * (
                                                                    self.ax_co2.get((t, n), 0) * self.MIU[t, n] + 
                                                                    self.bx_co2.get((t, n), 0) * self.MIU[t, n] ** 4)))

    def gdx_items(self):
        """ Handle the GDX items phase """
        print("GDX Items Phase")
        # List the items to be kept in the final gdx
        return self.miu_fixed_levels, self.miu_ndcs_2030


if __name__ == "__main__":
        
    # Example of how to use the class
    module = ModuleTemplate()

    # Run different phases
    module.conf()
    module.sets()
    module.include_data()
    module.compute_vars()
    module.before_solve()
    module.gdx_items()
