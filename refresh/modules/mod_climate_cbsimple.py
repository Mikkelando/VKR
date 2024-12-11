class ClimateModel:
    def __init__(self):
        # Настройки
        self.tcre = 1.6  # Transient Climate Response
        self.fex0 = 0.5  # 2015 forcings of non-CO2 GHG [Wm-2]
        self.fex1 = 1.0  # 2100 forcings of non-CO2 GHG [Wm-2]
        self.t2xco2 = 3.1  # Equilibrium temp impact [°C per doubling CO2]
        self.fco22x = 3.6813  # Forcings of equilibrium CO2 doubling (Wm-2)
        self.c10 = 0.098  # Initial climate equation coefficient for upper level
        self.c1beta = 0.01243  # Regression slope coefficient
        self.c1 = 0.1005  # Climate equation coefficient for upper level
        self.c3 = 0.088  # Transfer coefficient upper to lower stratum
        self.c4 = 0.025  # Transfer coefficient for lower level
        self.force2015 = 2.4634
        self.tatm2010 = 0.80
        self.tcorr = 0.3291984
        self.tatm0 = 0.80
        self.tocean0 = 0.0
        
        # Внешние параметры
        self.forcoth = {}  # Exogenous forcing from other greenhouse gases
        self.fcorr = 0  # Correction factor for Radiative Forcing
        self.force0ev = 0  # Starting forcing level

    def compute_forcoth(self, t):
        # OGHG forcing exogenous DICE-like
        if t < 18:
            return self.fex0 + (1/17) * (self.fex1 - self.fex0) * (t - 1)
        else:
            return self.fex1

    def compute_tcre_correction(self):
        # Transient TSC Correction
        return self.c10 + self.c1beta * (self.t2xco2 - 2.9)

    def compute_force0ev(self):
        # Compute initial forcing level
        return ((self.fco22x / self.t2xco2) * self.tatm2010) + \
               ((self.tatm0 - self.tatm2010) / self.c1) + \
               (self.c3 * (self.tatm2010 - self.tocean0))

    def compute_fcorr(self):
        self.force0ev = self.compute_force0ev()
        return 0.6 * (self.force2015 - self.force0ev)

    def eq_tatm(self, t, CCAETOT):
        # TEMPERATURE: Atmosphere
        forcoth_t = self.compute_forcoth(t)
        return CCAETOT * self.tcre / 1000 + 0.75 * forcoth_t - self.tcorr

    def eq_tocean(self, t, TATM, TOCEAN):
        # Ocean
        return TOCEAN + self.c4 * (TATM - TOCEAN)

    def eq_forc(self, t, TATM, TOCEAN):
        # Forcing
        forcoth_t = self.compute_forcoth(t)
        fcorr_t = self.compute_fcorr()
        return ((self.fco22x / self.t2xco2) * TATM) + \
               ((TATM - TATM) / self.c1) + \
               (self.c3 * (TATM - TOCEAN)) + \
               fcorr_t


# Пример использования:

climate_model = ClimateModel()

# Данные для вычислений
t = 20  # Пример года
CCAETOT = 1.0  # Примерное значение для CCAETOT
TATM = 0.85  # Примерное значение для TATM
TOCEAN = 0.80  # Примерное значение для TOCEAN

# Вычисления
tatm_value = climate_model.eq_tatm(t, CCAETOT)
tocean_value = climate_model.eq_tocean(t, TATM, TOCEAN)
forc_value = climate_model.eq_forc(t, TATM, TOCEAN)

print(f"TATM: {tatm_value}, TOCEAN: {tocean_value}, Forcing: {forc_value}")
