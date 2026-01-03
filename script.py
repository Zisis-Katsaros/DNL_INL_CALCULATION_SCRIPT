import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================== INITIALIZATION ============================== #
# Choose cvs file
FILENAME = 'out.csv'

# DAC Settings
width = 6 # = num of bits
Vref = 1.2
num_of_lvl = 2**width

def plot_dnl_inl(file_path):

    Vout_val = pd.read_csv(file_path)

    # Rename columns
    Vout_val.columns = ['Time', 'Voltage']

    # Drop any NaN values
    Vout_val = Vout_val.dropna()

    # Take the first 64 relevant ones
    voltages = Vout_val['Voltage'].values

    # Trim to 64 points if there are too many
    voltages = voltages[:num_of_lvl]

    # ============================== CALCULATIONS ============================== #

    # Determine LSB:
    # lsb = (Vmax -Vmin) / (num_of_steps - 1), calculated from the sample data instead of using theoretical value
    lsb = (voltages[-1] - voltages[0]) / (len(voltages) - 1)
    offset = voltages[0]

    # DNL Calculation:
    # dnl_i = (V_i - V_{i-1}) / lsb - 1
    dnl = []
    # dnl = 0 for code 0
    dnl.append(0.0)

    for i in range(1, len(voltages)):
        step_size = voltages[i] - voltages[i-1]
        dnl_val = (step_size / lsb) - 1
        dnl.append(dnl_val)

    # INL Calculation:
    # inl_i = (Vmeasured_i - Videal_i) / lsb
    inl = []
    for i in range(len(voltages)):
        Videal = offset + (i * lsb)
        inl_val = (voltages[i] - Videal) / lsb
        inl.append(inl_val)

    # ============================== RESULTS ============================== #
    dnl = np.array(dnl)
    inl = np.array(inl)

    dnl_max = np.max(dnl)
    dnl_min = np.min(dnl)
    inl_max = np.max(inl)
    inl_min = np.min(inl)

    print("------------------------------")
    print(f"DNLmax: {dnl_max:.4f} LSB")
    print(f"DNLmin: {dnl_min:.4f} LSB\n")
    print(f"INLmax: {inl_max:.4f} LSB")
    print(f"INLmin: {inl_min:.4f} LSB\n")


    # Check for DNL and INL +/- 1LSB specifiation:
    if abs(dnl_max) < 1.0 and abs(dnl_min) < 1.0:
        print("DNL: PASS")
    else:
        print("DNL: FAIL")

    if abs(inl_max) < 1.0 and abs(inl_min) < 1.0:
        print("INL: PASS")
    else:
        print("INL: FAIL")

    print("------------------------------")

    # ============================== GRAPH ============================== #
    codes = np.arange(len(voltages))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # DNL Plot
    ax1.plot(codes, dnl, marker='o', linestyle='-', color='blue', markersize=4)
    ax1.axhline(0, color='black', linewidth=0.8)
    ax1.axhline(1, color='red', linestyle='--', linewidth=0.8, label='Limit (+1)')
    ax1.axhline(-1, color='red', linestyle='--', linewidth=0.8, label='Limit (-1)')
    ax1.set_ylabel('DNL (LSB)')
    ax1.set_title('Differential Non-Linearity (DNL)')
    ax1.grid(True, which='both', linestyle='--', alpha=0.7)
    ax1.legend()

    # INL Plot
    ax2.plot(codes, inl, marker='s', linestyle='-', color='green', markersize=4)
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.axhline(1, color='red', linestyle='--', linewidth=0.8)
    ax2.axhline(-1, color='red', linestyle='--', linewidth=0.8)
    ax2.set_ylabel('INL (LSB)')
    ax2.set_xlabel('Code')
    ax2.set_title('Integral Non-Linearity (INL)')
    ax2.grid(True, which='both', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    plot_dnl_inl(FILENAME)