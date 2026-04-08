import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



import re
import math

def extract_geometry(header_lines):
    """
    Extracts initial length and cross-sectional area from header.
    
    Supports:
    - d0 → diameter → computes area
    - a0 → area directly
    - a0 + b0 → rectangular cross-section
    - Lc / L0 → initial length
    """

    length = None
    area = None

    d0 = None
    a0 = None
    b0 = None

    def extract_number(line):
        """Extract the numeric value from a header line.

        Uses the last matched numeric token so variable names like `d0` do not
        incorrectly return `0`.
        """
        matches = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", line)
        return float(matches[-1]) if matches else None

    for line in header_lines:
        l = line.lower()

        # Length
        if any(key in l for key in ["lc", "l0", "length"]):
            val = extract_number(line)
            if val is not None:
                length = val

        # Area directly
        elif "a0" in l and "mm" in l:
            val = extract_number(line)
            if val is not None:
                area = val

        # Diameter
        elif "d0" in l or "diameter" in l:
            val = extract_number(line)
            if val is not None:
                d0 = val

        # Rectangular sides
        elif "b0" in l:
            val = extract_number(line)
            if val is not None:
                b0 = val

        elif "width" in l or ("a0" in l and area is None):
            val = extract_number(line)
            if val is not None:
                a0 = val

    # ---- Compute area if missing ----
    if area is None:
        if d0 is not None:
            area = math.pi * (d0 ** 2) / 4
        elif a0 is not None and b0 is not None:
            area = a0 * b0

    # ---- Final check ----
    if length is None:
        raise ValueError("Could not determine initial length (Lc/L0).")

    if area is None:
        raise ValueError("Could not determine cross-sectional area (A0).")

    return length, area


def compute_stress_strain(data, length, area):
    """
    Converts displacement & force to strain & stress
    """
    displacement = data[:, 0]  # mm
    force = data[:, 1]         # N

    strain = displacement / length                  # dimensionless
    stress = force / area                          # N/mm^2 = MPa

    return strain, stress


def plot_stress_strain(strain, stress):
    plt.figure()
    plt.plot(strain, stress)
    plt.xlabel("Strain [-]")
    plt.ylabel("Stress [MPa]")
    plt.title("Stress-Strain Curve")
    plt.grid(True)
    plt.show()


def read_excel_file(file_path):
    """
    Reads data from an Excel file.
    Uses 'Results Specimen 1' to create header lines for geometry extraction.
    Uses 'Values Specimen 1' to read displacement and force values.
    Returns (header_lines, data).
    """
    # Read results sheet for geometry
    results_df = pd.read_excel(file_path, sheet_name='Results Specimen 1')

    header_lines = []
    if len(results_df) >= 2:
        units_row = results_df.iloc[0]
        values_row = results_df.iloc[1]
        for idx, col in enumerate(results_df.columns):
            if col in ["Unnamed: 0", "Specimen ID"]:
                continue
            value = values_row[col]
            if pd.isna(value):
                continue
            unit = units_row.iloc[idx]
            if pd.isna(unit):
                header_lines.append(f"{col} = {value}")
            else:
                header_lines.append(f"{col} = {value} {unit}")
    else:
        for col in results_df.columns:
            if col in ["Unnamed: 0", "Specimen ID"]:
                continue
            value = results_df.iloc[0][col]
            if pd.isna(value):
                continue
            header_lines.append(f"{col} = {value}")

    # Read values sheet for data
    values_df = pd.read_excel(file_path, sheet_name='Values Specimen 1')
    data = values_df.iloc[2:, [1, 2]].to_numpy(dtype=float)

    return header_lines, data


def main_excel(file_path):
    header, data = read_excel_file(file_path)
    length, area = extract_geometry(header)
    strain, stress = compute_stress_strain(data, length, area)
    print(area, length)
    plot_stress_strain(strain, stress)


if __name__ == "__main__":
    # Example usage
    main_excel("Uni_stuff\P2\Tension Rubber_2.xlsx")