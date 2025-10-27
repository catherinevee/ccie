# CCIE Network Configuration Repository for zwu

**IMPORTANT**: This is a **documentation-only repository**. It provides reference architecture, design patterns, configuration examples, and best practices for CCIE-level network deployments. The folder structure described below represents what a complete implementation should contain.

## Overview
This repository provides comprehensive documentation and reference materials for enterprise and service provider networks. Designed for CCIE-level study and implementation planning, it includes vendor-specific configuration examples, troubleshooting workflows, validation checklists, and design best practices for the zwu organization (`zwu.it.edu`).


## Project Structure
- **configs/**: Device-specific configuration files organized by role (spine, leaf, border, core), following zwu naming conventions.
- **templates/**: Jinja2 templates for generating configurations, annotated with real-world examples and best practices.
- **variables/**: YAML files defining global, device, and service-specific variables for reproducible deployments.
- **scripts/**: Python scripts for automated deployment, validation, rollback, and testing.
- **scripts/utils/**: Helper scripts for automation and validation.
- **ansible/**: Ansible playbooks and roles for automated configuration management and compliance enforcement.
- **documentation/**: Technical design documents, architecture diagrams, runbooks, and testing results.
- **docs/**: High-level guides, architecture overview, quick start, and reference links.
- **tests/**: Unit, integration, and fixture tests to ensure configuration correctness and operational readiness.
- **tools/**: Utility scripts for configuration building, validation, visualization, and compliance auditing.
- **bin/**: Executable scripts and tools.
- **ci/**: CI/CD pipeline configuration files.
- **.github/**: GitHub Actions workflows for automated testing and deployment.
- **CONTRIBUTING.md**: Contribution guidelines.
- **CODEOWNERS**: Code ownership and review assignments.


## Technology Use Cases: VXLAN, MPLS, and EVPN

**VXLAN**: Use for scalable Layer 2 overlays across Layer 3 networks, multi-tenant segmentation, and workload mobility in data centers. Ideal for extending VLANs over IP fabrics and supporting large numbers of segments.

**MPLS**: Use for efficient traffic engineering, fast reroute, and L2/L3 VPNs in service provider and large enterprise networks. Best for WAN connectivity, inter-data center transport, and isolated customer/service networks using VRFs and label switching.

**EVPN**: Use as a BGP-based control plane for VXLAN and MPLS overlays. Enables integrated L2/L3 services, multi-homing, MAC/IP route advertisement, and scalable overlays. Simplifies operations and supports seamless mobility and redundancy.

For technical details, configuration examples, and packet flow explanations, see:
- `documentation/design/fabric_reference.md`
- `documentation/design/topology.md`
- `documentation/design/vxlan_topology.md`
- `documentation/design/bgp_evpn_topology.md`

## Topology Diagram

Below is the zwu EVPN-VXLAN fabric topology, showing device roles, underlay/overlay protocols, and service integration:

![Network Topology](documentation/design/topology.png)

```
                +-------------------+        +-------------------+
                |    Spine 01       |        |    Spine 02       |
                | 10.77.0.1         |        | 10.77.0.2         |
                | OSPF/BGP-EVPN     |        | OSPF/BGP-EVPN     |
                +--------+----------+        +----------+--------+
                         | MPLS Core (LDP/SR)     |
                         |------------------------|
                +--------+----------+        +----------+--------+
                |    Leaf 01        |        |    Leaf 02        |
                | 10.77.0.11        |        | 10.77.0.12        |
                | OSPF/BGP-EVPN     |        | OSPF/BGP-EVPN     |
                | VXLAN VTEP        |        | VXLAN VTEP        |
                +--------+----------+        +----------+--------+
                         | VXLAN Overlay Fabric   |
                         |------------------------|
                +--------+----------+        +----------+--------+
                |    Leaf 03        |        |    Leaf 04        |
                | 10.77.0.13        |        | 10.77.0.14        |
                | OSPF/BGP-EVPN     |        | OSPF/BGP-EVPN     |
                | VXLAN VTEP        |        | VXLAN VTEP        |
                +--------+----------+        +----------+--------+
                         | Border/Edge (DCI/MPLS/EVPN) |
                         |------------------------------|
                +--------+----------+        +----------+--------+
                |   Border 01       |        |   Border 02       |
                | 10.77.0.21        |        | 10.77.0.22        |
                | OSPF/BGP-EVPN     |        | OSPF/BGP-EVPN     |
                | MPLS PE           |        | MPLS PE           |
                +-------------------+        +-------------------+
                         | MPLS/EVPN Interconnect |
                         |------------------------|
                +-------------------+        +-------------------+
                |      Core P01     |        |      Core P02     |
                |   10.77.0.31      |        |   10.77.0.32      |
                | MPLS P            |        | MPLS P            |
                +-------------------+        +-------------------+
                                |
                                |
                        +-------------------+
                        |      PE01         |
                        |   10.77.0.41      |
                        | MPLS PE           |
                        +-------------------+

Legend:
- OSPF: Underlay IGP for reachability
- BGP-EVPN: Overlay control plane for VXLAN
- VXLAN VTEP: Virtual Tunnel Endpoints for L2/L3 overlay
- MPLS Core: LDP/SR for transport, PE/P for VPN services
- Border: DCI, Inter-AS, or external connectivity
```

## Security and Compliance
- All configurations include AAA, SNMP, logging, NTP, SSH, and control plane policing.
- Access control lists and security banners are applied to all devices.
- Compliance scripts and standards are provided in `tools/compliance/`.

## Validation and Rollback
- Syntax validation and post-deployment verification commands are documented in each config.
- Rollback procedures are included for safe recovery.
- Automated validation scripts are available in `scripts/test/`.

## Setup Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ccie.git
   cd ccie
   ```

2. Install required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Review and customize variables in the `variables/` directory for your environment.

4. Generate and deploy configurations using the provided scripts and Ansible playbooks.

## Usage Guidelines
- Use Python scripts in `scripts/` for deployment, validation, and rollback.
- Customize Jinja2 templates in `templates/` for your specific requirements.
- Refer to documentation in `documentation/` for design, deployment, troubleshooting, and rollback instructions.
- Run tests in `tests/` before production deployment.

## Contribution
Contributions are welcome! Please submit a pull request or open an issue for enhancements, bug fixes, or new features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
Special thanks to the zwu network automation team and the broader network automation community for their contributions and support in developing this repository.
----------------------------------------