FILE: ccie/tests/integration/test_connectivity.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: test_connectivity.py
Purpose: This script performs integration tests to verify network connectivity between devices.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import sys
import subprocess
import yaml

def load_inventory(inventory_file):
    """Load device inventory from a YAML file."""
    with open(inventory_file, 'r') as file:
        return yaml.safe_load(file)

def ping_device(ip_address):
    """Ping a device to check connectivity."""
    try:
        output = subprocess.check_output(['ping', '-c', '3', ip_address], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def test_connectivity(devices):
    """Test connectivity to all devices in the inventory."""
    for device in devices:
        ip = device.get('ip')
        if ip:
            print(f"Pinging {ip}...")
            if ping_device(ip):
                print(f"Success: {ip} is reachable.")
            else:
                print(f"Failure: {ip} is not reachable.")

if __name__ == "__main__":
    inventory_file = os.path.join(os.path.dirname(__file__), '../ansible/inventory.yml')
    devices = load_inventory(inventory_file)
    test_connectivity(devices)
----------------------------------------