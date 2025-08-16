# CHANGELOG

## [Unreleased]
- Initial project setup with folder structure and basic files.

## [1.0.0] - 2023-10-01
### Added
- README.md for project documentation.
- .gitignore to specify files to ignore in Git.
- requirements.txt for Python dependencies.
- Makefile for automation commands.
- CHANGELOG.md to document version history.
- configs/ directory with subdirectories for spine, leaf, border, and core configurations.
- templates/ directory with Jinja2 templates for various configurations.
- variables/ directory for global and device-specific variables.
- scripts/ directory for automation scripts including deployment, generation, and testing.
- ansible/ directory for Ansible configuration and playbooks.
- documentation/ directory for design, runbooks, and testing documentation.
- tests/ directory for unit and integration tests.
- tools/ directory for utility scripts related to configuration building, visualization, and compliance.

## [1.0.1] - 2023-10-15
### Changed
- Updated README.md with detailed setup instructions and usage guidelines.
- Enhanced validation checks in configs/validation/ files for spine and leaf switches.
- Improved documentation in the design/ directory with additional diagrams and examples.

## [1.0.2] - 2023-10-30
### Fixed
- Resolved syntax issues in Python scripts within the scripts/ directory.
- Corrected YAML formatting in variables/ files for better compatibility with automation tools.

## [1.0.3] - 2023-11-15
### Added
- New Ansible playbooks for backup and rollback procedures.
- Additional test cases in tests/unit/ for improved coverage.

## [1.0.4] - 2023-11-30
### Changed
- Refined configuration templates in templates/ for better modularity and reusability.
- Updated deployment scripts to include logging and error handling features.

## [1.0.5] - 2023-12-15
### Removed
- Deprecated scripts that were no longer in use.
- Cleaned up unused variables in variables/ directory.

## [1.0.6] - 2024-01-01
### Security
- Implemented security best practices in configuration files.
- Added compliance checks in tools/compliance/ for auditing configurations.