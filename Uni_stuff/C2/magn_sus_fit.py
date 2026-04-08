import numpy as np
import matplotlib.pyplot as plt

def fit_susceptibility(delta_m, l, m_sample, molar_mass, chi_known):
    """
    delta_m: list or array of mass changes (kg)
    l: list or array of lengths (m)
    m_sample: list or array of sample masses (kg)
    molar_mass: list or array of molar masses (kg/mol)
    chi_known: list or array of known susceptibilities
    """

    # Convert to numpy arrays
    delta_m = np.array(delta_m)
    l = np.array(l)
    m_sample = np.array(m_sample)
    molar_mass = np.array(molar_mass)
    chi_known = np.array(chi_known)

    # Compute number of moles
    n = m_sample / molar_mass

    # Compute normalized variable
    X_raw = (delta_m * l) / n

    # Linear fit: chi = a * X_raw + b
    coeffs = np.polyfit(X_raw, chi_known, 1)
    a, b = coeffs

    # Generate fit line
    X_fit = np.linspace(min(X_raw), max(X_raw), 100)
    chi_fit = a * X_fit + b

    # Plot
    plt.figure()
    plt.scatter(X_raw, chi_known, label="Data")
    plt.plot(X_fit, chi_fit, label=f"Fit: χ = {a:.3e}·X + {b:.3e}")
    plt.xlabel("X_raw = (Δm · l) / n")
    plt.ylabel("Magnetic susceptibility χ")
    plt.legend()
    plt.title("Magnetic Susceptibility Calibration")
    plt.show()

    return a, b



delta_m1 = [
    -0.055e-3,   # NaCl
    -0.014e-3,   # Quartz
    -0.011e-3,   # CuSO4·5H2O
    -0.240e-3    # FeCl3·6H2O
]

l1 = [
    2.4e-2,   # NaCl
    2.44e-2,  # Quartz
    2.42e-2,  # CuSO4·5H2O
    2.36e-2   # FeCl3·6H2O
]

m_sample1 = [
    3.146e-3,  # NaCl
    3.94e-3,   # Quartz (SiO2)
    3.27e-3,   # CuSO4·5H2O
    3.54e-3    # FeCl3·6H2O
]

molar_mass1 = [
    58.44e-3,   # NaCl
    60.08e-3,   # SiO2
    249.68e-3,  # CuSO4·5H2O
    270.30e-3   # FeCl3·6H2O
]

chi_known1 = [
    -3.03e-5,   # NaCl
    -1.5e-5,    # Quartz
    1.76e-4,    # CuSO4·5H2O
    1.5e-2      # FeCl3·6H2O
]

delta_m2 = [
    -0.234e-3,  # Quartz

    -0.171e-3,  # FeSO4·7H2O
    +0.090e-3   # NaCl
]

l2 = [
    3.57e-2,  # Quartz

    3.8e-2,   # FeSO4·7H2O
    3.7e-2    # NaCl
]

m_sample2 = [
    4.517e-3,  # Quartz

    3.020e-3,  # FeSO4·7H2O
    3.600e-3   # NaCl
]

# molar masses in kg/mol
molar_mass2 = [
    60.08e-3,   # SiO2 (Quartz)

    278.01e-3,  # FeSO4·7H2O
    58.44e-3    # NaCl
]

chi_known2 = [
    -1.5e-5,   # Quartz

    1.2e-2,    # FeSO4·7H2O
    -3.03e-5   # NaCl
]
a1, b1 = fit_susceptibility(delta_m1, l1, m_sample1, molar_mass1, chi_known1)

a2, b2 = fit_susceptibility(delta_m2, l2, m_sample2, molar_mass2, chi_known2)

def predict_chi(delta_m, l, m_sample, molar_mass, a, b):
    n = m_sample / molar_mass
    X_raw = (delta_m * l) / n
    return a * X_raw + b


delta_m11 = [
    -0.110e-3,  # CaCl2
    0.023e-3,   # MgSO4
    0.017e-3    # BaSO4
]

l11 = [
    2.34e-2,  # CaCl2
    2.44e-2,  # MgSO4
    2.36e-2   # BaSO4
]

m_sample11 = [
    3.1e-3,   # CaCl2
    2.61e-3,  # MgSO4
    3.77e-3   # BaSO4
]

molar_mass11 = [
    110.98e-3,  # CaCl2
    120.37e-3,  # MgSO4 (assumed anhydrous!)
    233.39e-3   # BaSO4
]

# molar masses in kg/mol
molar_mass21 = [
    110.98e-3,  # CaCl2
    120.37e-3,  # MgSO4 (anhydrous assumption!)
    233.39e-3   # BaSO4
]
delta_m21 = [
    -0.202e-3,  # CaCl2
    0.014e-3,   # MgSO4
    -0.277e-3   # BaSO4
]

l21 = [
    3.53e-2,  # CaCl2
    3.1e-2,   # MgSO4
    3.52e-2   # BaSO4
]

m_sample21 = [
    3.4e-3,    # CaCl2
    2.865e-3,  # MgSO4
    3.477e-3   # BaSO4
]

# molar masses in kg/mol
molar_mass21 = [
    110.98e-3,  # CaCl2
    120.37e-3,  # MgSO4 (assumed anhydrous!)
    233.39e-3   # BaSO4
]
predicitons = []
for i in range(len(delta_m11)):
    predicitons.append(f"{predict_chi(delta_m11[i], l21[i], m_sample11[i], molar_mass11[i], a2, b2):e}") 
print(predicitons)