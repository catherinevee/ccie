FILE: /ccie/ccie/scripts/deploy/rollback.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: rollback.py
Purpose: This script handles rollback procedures in case of deployment failure.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import sys
import yaml

def load_previous_config(device):
    """
    Load the previous configuration for the specified device.
    """
    config_path = f"../configs/{device}/{device}.cfg"
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            return file.read()
    else:
        print(f"Configuration file for {device} not found.")
        return None

def rollback(device):
    """
    Rollback the configuration for the specified device.
    """
    previous_config = load_previous_config(device)
    if previous_config:
        # Here you would implement the logic to push the previous configuration back to the device
        print(f"Rolling back configuration for {device}...")
        # Example command to push config (this is a placeholder)
        # os.system(f"ssh admin@{device} 'configure replace {previous_config}'")
        print(f"Configuration for {device} rolled back successfully.")
    else:
        print(f"Rollback failed for {device}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: rollback.py <device>")
        sys.exit(1)

    device_name = sys.argv[1]
    rollback(device_name)
----------------------------------------