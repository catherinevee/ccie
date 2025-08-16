FILE: /ccie/ccie/tests/unit/test_variables.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: test_variables.py
Purpose: Unit tests for configuration variables
Author: zwu Network Automation Team
Date: [Date]
"""

import unittest
import yaml

class TestVariables(unittest.TestCase):
    def setUp(self):
        """Load the YAML variable files for testing."""
        with open('../variables/global_vars.yml', 'r') as file:
            self.global_vars = yaml.safe_load(file)
        with open('../variables/fabric_vars.yml', 'r') as file:
            self.fabric_vars = yaml.safe_load(file)
        # Load device-specific variables
        self.device_vars = {}
        for device in ['spine01', 'spine02', 'leaf01', 'leaf02']:
            with open(f'../variables/devices/{device}.yml', 'r') as file:
                self.device_vars[device] = yaml.safe_load(file)

    def test_global_vars(self):
        """Test global variables for expected values."""
        self.assertIn('some_global_variable', self.global_vars)
        self.assertEqual(self.global_vars['some_global_variable'], 'expected_value')

    def test_fabric_vars(self):
        """Test fabric-wide settings."""
        self.assertIn('fabric_name', self.fabric_vars)
        self.assertEqual(self.fabric_vars['fabric_name'], 'expected_fabric_name')

    def test_device_vars(self):
        """Test device-specific variables."""
        for device in self.device_vars:
            self.assertIn('hostname', self.device_vars[device])
            self.assertTrue(self.device_vars[device]['hostname'].startswith(device))

if __name__ == '__main__':
    unittest.main()
----------------------------------------