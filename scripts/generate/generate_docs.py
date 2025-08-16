FILE: /ccie/ccie/scripts/generate/generate_docs.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: generate_docs.py
Purpose: This script generates documentation for the network configuration project.
Author: zwu Network Automation Team
Date: [Date]
"""

import os
import markdown
from pathlib import Path

def generate_readme():
    """Generate README.md documentation."""
    readme_content = """
# Network Configuration Project

## Overview
This project contains network configurations for enterprise and service provider networks, utilizing infrastructure-as-code principles.

## Setup Instructions
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Run the deployment scripts as needed.

## Usage Guidelines
- Use the `scripts/deploy/deploy.py` to apply configurations.
- Validate configurations with `scripts/deploy/validate.py`.
- Rollback configurations using `scripts/deploy/rollback.py`.
"""
    with open('README.md', 'w') as f:
        f.write(readme_content.strip())

def generate_changelog():
    """Generate CHANGELOG.md documentation."""
    changelog_content = """
# Changelog

## [Unreleased]
- Initial project setup with basic configurations and scripts.

## [1.0.0] - [Date]
- Added support for EVPN-VXLAN configurations.
- Implemented validation and rollback scripts.
"""
    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog_content.strip())

def generate_documentation():
    """Generate all documentation files."""
    generate_readme()
    generate_changelog()
    print("Documentation generated successfully.")

if __name__ == "__main__":
    generate_documentation()
----------------------------------------