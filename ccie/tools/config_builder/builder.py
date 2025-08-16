FILE: /ccie/tools/config_builder/builder.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: builder.py
Purpose: This script builds network configurations based on templates and variables.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import yaml
from jinja2 import Environment, FileSystemLoader

def load_variables(variable_file):
    """Load variables from a YAML file."""
    with open(variable_file, 'r') as file:
        return yaml.safe_load(file)

def render_template(template_file, context):
    """Render a Jinja2 template with the given context."""
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_file)
    return template.render(context)

def build_configuration(device_name, template_name, variable_file):
    """Build the configuration for a specific device."""
    variables = load_variables(variable_file)
    configuration = render_template(template_name, variables)
    
    output_file = f'configs/{device_name}.cfg'
    with open(output_file, 'w') as file:
        file.write(configuration)
    
    print(f'Configuration for {device_name} has been written to {output_file}')

if __name__ == "__main__":
    # Example usage
    devices = {
        'spine01': 'evpn/evpn_spine.j2',
        'leaf01': 'evpn/evpn_leaf.j2',
        'border01': 'evpn/evpn_border.j2'
    }
    
    for device, template in devices.items():
        variable_file = f'variables/devices/{device}.yml'
        build_configuration(device, template, variable_file)
----------------------------------------