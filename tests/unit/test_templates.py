FILE: /ccie/ccie/tests/unit/test_templates.py
----------------------------------------
import unittest
from jinja2 import Environment, FileSystemLoader

class TestTemplates(unittest.TestCase):
    def setUp(self):
        # Set up the Jinja2 environment for loading templates
        self.env = Environment(loader=FileSystemLoader('templates'))

    def test_cisco_base_template(self):
        # Test rendering of the Cisco base template
        template = self.env.get_template('base/cisco_base.j2')
        rendered = template.render(hostname='spine01', domain='example.com')
        
        # Validate the rendered output
        self.assertIn('hostname spine01', rendered)
        self.assertIn('domain-name example.com', rendered)

    def test_juniper_base_template(self):
        # Test rendering of the Juniper base template
        template = self.env.get_template('base/juniper_base.j2')
        rendered = template.render(hostname='leaf01', domain='example.com')
        
        # Validate the rendered output
        self.assertIn('host-name leaf01;', rendered)
        self.assertIn('domain-name example.com;', rendered)

    def test_evpn_leaf_template(self):
        # Test rendering of the EVPN leaf template
        template = self.env.get_template('evpn/evpn_leaf.j2')
        rendered = template.render(leaf_id='leaf01', vni='10010', vlan='10')
        
        # Validate the rendered output
        self.assertIn('vni 10010', rendered)
        self.assertIn('bridge-domain 10', rendered)

    def test_mpls_pe_template(self):
        # Test rendering of the MPLS PE template
        template = self.env.get_template('mpls/mpls_pe.j2')
        rendered = template.render(pe_id='pe01', vrf='VRF1')
        
        # Validate the rendered output
        self.assertIn('vrf VRF1', rendered)
        self.assertIn('interface GigabitEthernet0/0', rendered)

if __name__ == '__main__':
    unittest.main()
----------------------------------------