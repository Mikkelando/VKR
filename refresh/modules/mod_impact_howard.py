import numpy as np

# DICE-2016-like impact parameters
a1 = 0         # Damage intercept
a2 = 0.595     # Damage quadratic term
a3 = 2.00      # Damage exponent

# Adjust for catastrophic damages (25% increase in a2)
a2 *= 1.25

# Convert a2 to percentages
a2 /= 100

# Example temperature data (replace with actual data or computation)
TATM = np.array([1.0, 1.5, 2.0])  # Example temperature values (can be from actual model)

# Variables (based on the original model)
OMEGA = np.zeros_like(TATM)  # Initializing OMEGA variable with zeros

# Function to compute OMEGA based on Howard and Sterner's impact specification
def compute_omega(TATM):
    for t in range(1, len(TATM)):  # Starting from time step 1 (excluding tfirst)
        OMEGA[t] = (a1 * TATM[t]) + (a2 * (TATM[t] ** a3)) - (a1 * TATM[1]) - (a2 * (TATM[1] ** a3))
    return OMEGA

if __name__ == "__main__":
    OMEGA = compute_omega(TATM)

    # Reporting of results (for GDX items or equivalent)
    print(f"Damage Intercept (a1): {a1}")
    print(f"Damage Quadratic Term (a2) after catastrophic adjustment and conversion to percentage: {a2}")
    print(f"Damage Exponent (a3): {a3}")
    print(f"OMEGA: {OMEGA}")
