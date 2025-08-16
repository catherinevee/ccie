FILE: /ccie/ccie/scripts/deploy/validate.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: validate.py
Purpose: Validate the configurations after deployment.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import sys
import yaml

def load_checks(check_file):
    """Load validation checks from a YAML file."""
    with open(check_file, 'r') as file:
        return yaml.safe_load(file)

def validate_configuration(config_file, checks):
    """Validate the configuration against the provided checks."""
    with open(config_file, 'r') as file:
        config = file.read()
    
    # Perform validation checks
    for check in checks:
        if check not in config:
            print(f"Validation failed: {check} not found in {config_file}")
            return False
    return True

def main():
    """Main function to validate configurations."""
    # Define the paths to configuration and checks
    config_paths = [
        'configs/spine/spine01.cfg',
        'configs/spine/spine02.cfg',
        'configs/leaf/leaf01.cfg',
        'configs/leaf/leaf02.cfg',
        'configs/leaf/leaf03.cfg',
        'configs/leaf/leaf04.cfg',
        'configs/border/border01.cfg',
        'configs/border/border02.cfg',
        'configs/core/p01.cfg',
        'configs/core/p02.cfg',
        'configs/core/pe01.cfg'
    ]
    
    check_files = [
        'configs/spine/validation/spine01_checks.yml',
        'configs/spine/validation/spine02_checks.yml',
        'configs/leaf/validation/leaf_checks.yml',
        'configs/border/validation/border_checks.yml'
    ]

    # Validate each configuration file
    for config_file in config_paths:
        checks = load_checks(check_files[0])  # Load checks for spine as an example
        if not validate_configuration(config_file, checks):
            print(f"Validation failed for {config_file}")
            sys.exit(1)

    print("All configurations validated successfully.")

if __name__ == "__main__":
    main()
----------------------------------------