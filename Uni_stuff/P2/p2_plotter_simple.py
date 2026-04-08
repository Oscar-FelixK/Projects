import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Lookup table: filename -> (length [mm], area [mm^2])
# Fill in your measured/known values here
MATERIAL_GEOMETRY = {
    "Aluminium Bar _1.xlsx": (21.6, 7.069),  # length [mm], area [mm2]
    "Polystyrene Tension_1.xlsx": (75, 10*4),
    "Polystyrene_Compression_1.xlsx": (16.91229822, 50.265482),
    "Tension Rubber_1.xlsx": (31.1606544, 1.3*2.4),
    "Tension Rubber_2.xlsx": (35.11196859, 1.3*2.4),
    "Tension_HDPE Tension_1.xlsx": (15, 0.66),
    "Tension_LDPE Tension_1.xlsx": (15, 4*0.222),
    "Topas COC Tension_1.xlsx": (75, 10*4),
    "UHMWPE Dyneema Fiber_1.xlsx": (93.6, 1.07513e-4),
}


def extract_data_from_excel(file_path):
    """
    Extracts displacement and force data from Excel file.
    Works with sheets named 'Values Specimen 1', 'Values Specimen 2', 'Values Specimen 3', etc.
    Returns (displacement, force) as numpy arrays.
    """
    xls = pd.ExcelFile(file_path)
    candidate_sheets = [name for name in xls.sheet_names if 'values specimen' in name.lower()]
    if not candidate_sheets:
        raise ValueError(f"No 'Values Specimen' sheet found in {file_path}")

    sheet_name = candidate_sheets[0]
    values_df = pd.read_excel(file_path, sheet_name=sheet_name)
    # Skip first two rows (headers), take columns 0 and 1 (displacement and force)
    if file_path == r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Aluminium Bar _1.xlsx":  ##alu has 3 datasets, displacement, grip to grip and force
        data = values_df.iloc[2:, [0, 2]].to_numpy(dtype=float)
        displacement = data[:, 0]
        force = data[:, 1]
    else:
        data = values_df.iloc[2:, [0, 1]].to_numpy(dtype=float)
        displacement = data[:, 0]
        force = data[:, 1]
    return displacement, force


def compute_stress_strain(displacement, force, length, area):
    """
    Converts displacement & force to strain & stress.
    """
    strain = displacement / length
    stress = force / area
    tensile_strength = np.max(stress)
    print(f"tensile strength: {round(tensile_strength,2)}")
    return strain, stress


def plot_stress_strain(strain, stress, title="Stress-Strain Curve"):
    """
    Plots stress vs strain curve.
    """

    plt.figure()
    plt.plot(strain, stress, linewidth=1.5)
    plt.xlabel("Strain [-]")
    plt.ylabel("Stress [MPa]")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.show()

import matplotlib.pyplot as plt



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def interactive_analysis(strain, stress,filename):
    selected_points = []
    E = None
    offset = 0.002  # 0.2% strain offset

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)  # space for buttons

    ax.plot(strain, stress, label="Stress-Strain")
    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (MPa)")
    ax.set_title(f"Youngs Modulus Fit {filename}")

    ax.grid(True)

    # Store original limits for zoom reset
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()

    def onclick(event):
        nonlocal selected_points, E

        if event.xdata is None:
            return

        # ---- Step 1: Elastic region ----
        if len(selected_points) < 2:
            selected_points.append(event.xdata)
            ax.axvline(event.xdata, color='r', linestyle='--')
            fig.canvas.draw()

            if len(selected_points) == 2:
                x1, x2 = sorted(selected_points)

                mask = (strain >= x1) & (strain <= x2)
                x = strain[mask]
                y = stress[mask]

                coeffs = np.polyfit(x, y, 1)
                E = coeffs[0]

                # Plot fit
                y_fit = np.polyval(coeffs, x)
                ax.plot(x, y_fit, 'g', label=f"E = {E:.2f} MPa")

                # Offset line
                offset_line = E * (strain - offset)
                ax.plot(strain, offset_line, 'orange', linestyle='--', label="0.2% offset")

                ax.legend()
                fig.canvas.draw()

                print(f"Young's Modulus E = {E:.2f} MPa")

        # ---- Step 2: Yield point ----
        elif len(selected_points) == 2:
            distances = np.abs(strain - event.xdata)
            idx = np.argmin(distances)

            yield_strain = strain[idx]
            yield_stress = stress[idx]

            ax.plot(yield_strain, yield_stress, 'ro', label="Yield Point")
            ax.legend()

            # 🔄 Reset zoom to original
            ax.set_xlim(original_xlim)
            ax.set_ylim(original_ylim)

            fig.canvas.draw()

            print(f"Yield Stress = {yield_stress:.2f} MPa")
            print(f"Yield Strain = {yield_strain:.6f}")

            selected_points.append("done")

    fig.canvas.mpl_connect('button_press_event', onclick)

    # ---- Quit button ----
    ax_quit = plt.axes([0.8, 0.05, 0.1, 0.075])
    btn_quit = Button(ax_quit, 'Quit')

    def quit_event(event):
        plt.close(fig)

    btn_quit.on_clicked(quit_event)

    plt.show()
def process_material(file_path, filename):
    """
    Process a single material file: extract data, compute stress-strain, and plot.
    """
    if filename not in MATERIAL_GEOMETRY:
        print(f"Warning: {filename} not in lookup table. Skipping.")
        return
    
    length, area = MATERIAL_GEOMETRY[filename]
    if length is None or area is None:
        print(f"Warning: {filename} has missing geometry (length={length}, area={area}). Skipping.")
        return
    
    displacement, force = extract_data_from_excel(file_path)
    strain, stress = compute_stress_strain(displacement, force, length, area)
    interactive_analysis(strain, stress, filename)

   # plot_stress_strain(strain, stress, title=filename.replace(".xlsx", ""))

materils_list = [
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Aluminium Bar _1.xlsx", "Aluminium Bar _1.xlsx"], #0
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Polystyrene Tension_1.xlsx", "Polystyrene Tension_1.xlsx"], #1
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Polystyrene_Compression_1.xlsx", "Polystyrene_Compression_1.xlsx"], #2
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Tension Rubber_1.xlsx", "Tension Rubber_1.xlsx"], #3
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Tension Rubber_2.xlsx", "Tension Rubber_2.xlsx"], #4
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Tension_HDPE Tension_1.xlsx", "Tension_HDPE Tension_1.xlsx"], #5
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Tension_LDPE Tension_1.xlsx", "Tension_LDPE Tension_1.xlsx"], #6
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\Topas COC Tension_1.xlsx", "Topas COC Tension_1.xlsx"], #7
    [r"C:\Users\oscar\Projects-3\Uni_stuff\P2\UHMWPE Dyneema Fiber_1.xlsx", "UHMWPE Dyneema Fiber_1.xlsx"] #8
]  #filepath, name

if __name__ == "__main__":
    # Example: process one file
    for i in range(len(materils_list)):
        process_material(materils_list[i][0], materils_list[i][1])