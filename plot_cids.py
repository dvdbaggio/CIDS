import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def run_cids_analysis(log_file, attack_name, target_id="188"):
    if not os.path.exists(log_file):
        return print(f"File {log_file} not found.")

    cids_dir = "./CIDS"
    if not os.path.exists(cids_dir):
        os.makedirs(cids_dir)

    timestamps = []
    with open(log_file, 'r') as f:
        for line in f:
            if f" {target_id}#" in line:
                try:
                    ts = float(line.split('(')[1].split(')')[0])
                    timestamps.append(ts)
                except:
                    continue
    
    if len(timestamps) < 1500:
        return print("Insufficient data. The experiment must last at least 30 seconds.")

    time_seconds = np.array(timestamps[1:]) - timestamps[0]
    intervals = np.diff(timestamps)
    
    # CIDS parameters
    T_ref = 0.020
    S, P, lam = 0.0, 1.0, 0.9995
    L_plus = 0.0
    std_err = 0.0001 
    kappa = 0.001    
    
    O_acc = 0.0
    errors, cusum_h = [], []

    for i, dt in enumerate(intervals):
        offset = dt - T_ref
        O_acc += abs(offset)
        t = i + 1
        
        if i < 1500:
            error = O_acc - S * t
            gain = P * t / (lam + t**2 * P)
            P = (P - gain * t * P) / lam
            S = S + gain * error
        else:
            error = O_acc - S * t
        
        L_plus = max(0, L_plus + (abs(error) / std_err) - kappa)
        errors.append(error)
        cusum_h.append(L_plus)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax1.plot(time_seconds, errors, color='blue', linewidth=0.7)
    ax1.set_title(f'CIDS Analysis: {attack_name.upper()} Attack (ID 0x{target_id})', fontsize=14)
    ax1.set_ylabel('Identification Error [s]', fontweight='bold')
    ax1.grid(True, alpha=0.3)

    ax2.plot(time_seconds, cusum_h, color='red', label='CUSUM (L+)')
    ax2.axhline(y=5.0, color='black', linestyle='--', label='Threshold Gamma=5')
    ax2.set_ylabel('CUSUM Value', fontweight='bold')
    ax2.set_xlabel('Time [seconds]', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(cids_dir, f"cids_{attack_name}.png")
    plt.savefig(output_path, dpi=300)
    print(f"Plot saved in: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Using: python3 plot_cids.py <file_log> <attack_name>")
    else:
        log_input = sys.argv[1]
        atk_input = sys.argv[2]
        run_cids_analysis(log_input, atk_input)