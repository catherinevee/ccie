FILE: /ccie/ccie/scripts/generate/generate_configs.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: generate_configs.py
Purpose: Generate device configurations based on templates and variables.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import yaml
from jinja2 import Environment, FileSystemLoader

def load_variables(variable_file):
    """Load YAML variables from a specified file."""
    with open(variable_file, 'r') as file:
        return yaml.safe_load(file)

def render_template(template_file, context):
    """Render a Jinja2 template with the given context."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_file)
    return template.render(context)

def generate_config(device_name, device_vars):
    """Generate configuration for a specific device."""
    # Determine the template based on device role
    role = device_vars.get('role')
    if role == 'spine':
        template_file = 'evpn/evpn_spine.j2'
    elif role == 'leaf':
        template_file = 'evpn/evpn_leaf.j2'
    elif role == 'border':
        template_file = 'evpn/evpn_border.j2'
    else:
        raise ValueError(f"Unknown role: {role}")

    # Render the configuration
    config = render_template(template_file, device_vars)
    config_file_path = os.path.join('configs', role, f"{device_name}.cfg")

    # Write the configuration to a file
    with open(config_file_path, 'w') as config_file:
        config_file.write(config)

def main():
    """Main function to generate configurations for all devices."""
    # Load global variables
    global_vars = load_variables('../variables/global_vars.yml')

    # Load device-specific variables
    devices = ['spine01', 'spine02', 'leaf01', 'leaf02', 'leaf03', 'leaf04', 'border01', 'border02']
    for device in devices:
        device_vars = load_variables(f'../variables/devices/{device}.yml')
        device_vars.update(global_vars)  # Merge global variables into device-specific variables
        generate_config(device, device_vars)

if __name__ == "__main__":
    main()
----------------------------------------