#!/usr/bin/env python3
"""
RF Noise at 433.92 MHz on boot - Fixed for HDMI monitor
"""

import subprocess
import time
import sys
import os

def run_command(cmd, description):
    print(f"[+] {description}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode != 0:
            print(f"    Warning: {result.stderr.strip()}")
        return result.returncode == 0
    except:
        return False

def main():
    print("=== RF Noise Boot Script Started (kira) ===")
    
    # === Fix HDMI issues before starting rpitx ===
    print("[1/3] Applying HDMI stability fixes...")
    run_command(["vcgencmd", "force_audio", "0"], "Disable audio")
    run_command(["vcgencmd", "hdmi_timings", "0"], "Reset HDMI")
    
    time.sleep(2)

    # Start rpitx-ui (optional, can comment out if you don't need the menu)
    print("[2/3] Starting rpitx-ui...")
    subprocess.Popen(["rpitx-ui"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(4)

    # Start noise generation
    print("[3/3] Starting 433.92 MHz noise generator...")
    
    cmd = [
        "sudo", "pirfgen",
        "433920000",      # 400 MHz
        "8000000",        # 8 MHz bandwidth (reduced to help stability)
        "-m", "noise",
        "-s", "500000"
    ]
    
    try:
        process = subprocess.Popen(cmd, 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
        print(f"[✓] Noise transmitter started (PID {process.pid})")
        print("    Monitor should stay on now.")
        
        # Keep script alive
        while True:
            time.sleep(300)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    main()
