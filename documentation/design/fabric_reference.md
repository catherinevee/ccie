# zwu Fabric Technology Reference

This document provides concise technical overviews, configuration examples, packet flow explanations, validation steps, and best practices for VXLAN, MPLS, and EVPN in the zwu network fabric.

---

## 1. Technology Overviews

### VXLAN
VXLAN (Virtual Extensible LAN) is a network virtualization technology that enables scalable Layer 2 overlays across Layer 3 networks using MAC-in-UDP encapsulation. It uses VTEPs (VXLAN Tunnel Endpoints) and VNIs (VXLAN Network Identifiers) to segment traffic.

### MPLS
MPLS (Multiprotocol Label Switching) is a protocol for efficient packet forwarding using labels instead of IP addresses. It supports L2/L3 VPNs, traffic engineering, and fast reroute. Key components include LDP/SR, PE/P routers, and VRFs.

### EVPN
EVPN (Ethernet VPN) is a BGP-based control plane for VXLAN and MPLS, providing MAC/IP route advertisement, multi-homing, and integrated L2/L3 services. It uses BGP sessions, route reflectors, and NLRI for scalable overlays.

---

## 2. Topology Diagrams
- See `topology.md` (overall fabric)
- See `vxlan_topology.md` (VXLAN data plane)
- See `bgp_evpn_topology.md` (EVPN control plane)

---

## 3. Configuration Examples

### VXLAN (Leaf Switch)
```
interface Vxlan1
  vxlan source-interface Loopback0
  vxlan udp-port 4789
  vxlan vlan 100 vni 5000
  vxlan vlan 102 vni 5002
  vxlan mcast-group 239.1.1.1
```

### MPLS (Core Router)
```
router ospf 1
  network 10.77.0.0 0.0.0.255 area 0
mpls ldp
  router-id Loopback0
  interface Eth1/1
ip vrf CustomerA
  rd 100:1
  route-target export 100:1
  route-target import 100:1
```

### EVPN (Leaf/Spine)
```
router bgp 65000
  address-family l2vpn evpn
    neighbor 10.77.0.1 remote-as 65000
    advertise-all-vni
```

---

## 4. Packet Flow Explanations
- See `topology.md` and `vxlan_topology.md` for end-to-end packet walkthroughs.

---

## 5. Control/Data Plane Details
- Control plane: OSPF (underlay), BGP (EVPN), LDP/SR (MPLS)
- Data plane: VXLAN encapsulation, MPLS label switching, IP forwarding

---

## 6. Validation and Troubleshooting
- Validate VXLAN overlays: `show vxlan interface`, `show mac address-table vni`
- Validate MPLS paths: `show mpls ldp neighbor`, `show mpls forwarding-table`
- Validate EVPN: `show bgp l2vpn evpn route`, `show bgp neighbor`
- Troubleshoot: Check control plane adjacencies, encapsulation, and route advertisements

---

## 7. Testing and Automation
- Use Ansible playbooks in `ansible/playbooks/` for automated deployment and validation
- Run unit/integration tests in `tests/`

---

## 8. Best Practices and Security
- Enable AAA, SNMP, logging, NTP, SSH, and control plane policing
- Apply ACLs and security banners to all devices
- Use redundant route reflectors and ECMP for high availability
- Segment services with VRFs and VNIs

---

## 9. Glossary and References
- VXLAN: Virtual Extensible LAN
- VTEP: VXLAN Tunnel Endpoint
- VNI: VXLAN Network Identifier
- MPLS: Multiprotocol Label Switching
- LDP: Label Distribution Protocol
- SR: Segment Routing
- EVPN: Ethernet VPN
- NLRI: Network Layer Reachability Information
- RFCs: [RFC 7348 (VXLAN)](https://datatracker.ietf.org/doc/html/rfc7348), [RFC 7432 (EVPN)](https://datatracker.ietf.org/doc/html/rfc7432)

---

For further details, see the referenced topology and configuration files in this repository.
