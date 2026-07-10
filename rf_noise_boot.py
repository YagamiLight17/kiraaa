#!/usr/bin/env python3


import subprocess
import time
import sys
import os

def run_command(cmd, description):
    print(f"[+] {description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"[!] Warning: {description} failed with code {result.returncode}")
            print(result.stderr)
        else:
            print(f"[✓] {description} completed.")
        return result
    except Exception as e:
        print(f"[!] Error running {description}: {e}")
        return None

def main():
    print("=== Raspberry Pi RF Noise Generator Boot Script ===")
    print(f"Running as user: kira")
    
    # 1. Run rpitx-ui
    print("[1/3] Starting rpitx-ui...")
    run_command(["rpitx-ui"], "rpitx-ui launcher")
    time.sleep(3)

    # 2. Start RF noise at 433.92 MHz
    freq = 433_920_000      # 433.92 MHz
    bandwidth = 10_000_000  # 10 MHz bandwidth (adjustable)
    sample_rate = 500_000

    print(f"[2/3] Starting noise generation at {freq/1e6} MHz...")
    
    cmd = [
        "sudo", "pirfgen",
        str(freq),
        str(bandwidth),
        "-m", "noise",
        "-s", str(sample_rate)
    ]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[✓] pirfgen started with PID {process.pid} → Noise transmitting at 400 MHz")
        
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nStopping transmitter...")
            process.terminate()
    except FileNotFoundError:
        print("[!] 'pirfgen' not found. Install rpitx-ui first.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Re-running with sudo...")
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    main()
