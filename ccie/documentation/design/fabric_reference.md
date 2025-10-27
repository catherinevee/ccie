# zwu Fabric Technology Reference

This document provides comprehensive technical overviews, vendor-specific configuration examples, packet flow explanations, validation steps, and best practices for VXLAN, MPLS, and EVPN in the zwu network fabric.

**Note**: This is a reference architecture guide. Configurations are examples and must be adapted for your specific vendor platform and environment requirements.

---

## 1. Technology Overviews

### VXLAN
VXLAN (Virtual Extensible LAN) is a network virtualization technology that enables scalable Layer 2 overlays across Layer 3 networks using MAC-in-UDP encapsulation. It uses VTEPs (VXLAN Tunnel Endpoints) and VNIs (VXLAN Network Identifiers) to segment traffic.

**Key Features**:
- Supports up to 16 million segments (24-bit VNI vs 12-bit VLAN ID)
- UDP port 4789 (IANA assigned)
- Operates over Layer 3 underlay network
- Enables workload mobility across data centers

### MPLS
MPLS (Multiprotocol Label Switching) is a protocol for efficient packet forwarding using labels instead of IP addresses. It supports L2/L3 VPNs, traffic engineering, and fast reroute. Key components include LDP/SR, PE/P routers, and VRFs.

**Label Operations**:
- **Push**: Add MPLS label to packet (ingress PE)
- **Swap**: Replace incoming label with outgoing label (P routers)
- **Pop**: Remove MPLS label (egress PE or penultimate hop)

### EVPN
EVPN (Ethernet VPN) is a BGP-based control plane for VXLAN and MPLS, providing MAC/IP route advertisement, multi-homing, and integrated L2/L3 services. It uses BGP sessions, route reflectors, and NLRI for scalable overlays.

**EVPN Route Types**:
- **Type 1**: Ethernet Auto-Discovery (A-D) route
- **Type 2**: MAC/IP Advertisement route (most common)
- **Type 3**: Inclusive Multicast Ethernet Tag (IMET) route
- **Type 4**: Ethernet Segment route
- **Type 5**: IP Prefix route (for L3 EVPN)

---

## 2. Topology Diagrams
- See `topology.md` (overall fabric)
- See `vxlan_topology.md` (VXLAN data plane)
- See `bgp_evpn_topology.md` (EVPN control plane)

---

## 3. Configuration Examples

### 3.1 VXLAN with EVPN (Leaf Switch)

**Important**: Modern EVPN-VXLAN fabrics use **ingress replication** for BUM traffic, not multicast.

#### Arista EOS
```
interface Vxlan1
  vxlan source-interface Loopback1
  vxlan udp-port 4789
  vxlan vlan 100 vni 10100
  vxlan vlan 102 vni 10102
  vxlan flood vtep ingress-replication

interface Loopback1
  ip address 10.77.0.11/32

router bgp 65000
  neighbor SPINE peer group
  neighbor SPINE remote-as 65000
  neighbor SPINE update-source Loopback0
  neighbor SPINE send-community extended
  neighbor 10.77.0.1 peer group SPINE
  neighbor 10.77.0.2 peer group SPINE
  !
  address-family evpn
    neighbor SPINE activate
  !
  vlan 100
    rd 10.77.0.11:100
    route-target both 65000:10100
    redistribute learned
  !
  vlan 102
    rd 10.77.0.11:102
    route-target both 65000:10102
    redistribute learned
```

#### Cisco NX-OS
```
feature nv overlay
feature vn-segment-vlan-based

vlan 100
  vn-segment 10100
vlan 102
  vn-segment 10102

interface nve1
  no shutdown
  source-interface loopback1
  host-reachability protocol bgp
  member vni 10100
    ingress-replication protocol bgp
  member vni 10102
    ingress-replication protocol bgp

interface loopback1
  ip address 10.77.0.11/32

router bgp 65000
  neighbor 10.77.0.1 remote-as 65000
    update-source loopback0
    address-family l2vpn evpn
      send-community extended
  neighbor 10.77.0.2 remote-as 65000
    update-source loopback0
    address-family l2vpn evpn
      send-community extended

evpn
  vni 10100 l2
    rd auto
    route-target import auto
    route-target export auto
  vni 10102 l2
    rd auto
    route-target import auto
    route-target export auto
```

#### Juniper Junos
```
set interfaces lo0 unit 1 family inet address 10.77.0.11/32

set protocols bgp group EVPN-OVERLAY type internal
set protocols bgp group EVPN-OVERLAY local-address 10.77.0.11
set protocols bgp group EVPN-OVERLAY family evpn signaling
set protocols bgp group EVPN-OVERLAY neighbor 10.77.0.1
set protocols bgp group EVPN-OVERLAY neighbor 10.77.0.2

set vlans VLAN100 vlan-id 100
set vlans VLAN100 vxlan vni 10100
set vlans VLAN100 vxlan ingress-node-replication

set vlans VLAN102 vlan-id 102
set vlans VLAN102 vxlan vni 10102
set vlans VLAN102 vxlan ingress-node-replication

set routing-instances EVPN-VXLAN instance-type virtual-switch
set routing-instances EVPN-VXLAN route-distinguisher 10.77.0.11:1
set routing-instances EVPN-VXLAN vrf-target target:65000:1
set routing-instances EVPN-VXLAN protocols evpn
```

---

### 3.2 BGP Route Reflector Configuration (Spine)

#### Arista EOS
```
router bgp 65000
  bgp listen range 10.77.0.0/24 peer-group EVPN-CLIENTS remote-as 65000
  neighbor EVPN-CLIENTS peer group
  neighbor EVPN-CLIENTS update-source Loopback0
  neighbor EVPN-CLIENTS route-reflector-client
  neighbor EVPN-CLIENTS send-community extended
  !
  address-family evpn
    neighbor EVPN-CLIENTS activate
    neighbor EVPN-CLIENTS route-reflector-client
```

#### Cisco NX-OS
```
router bgp 65000
  template peer-policy RR-CLIENT
    send-community extended
    route-reflector-client

  neighbor 10.77.0.11 remote-as 65000
    update-source loopback0
    address-family l2vpn evpn
      send-community extended
      route-reflector-client

  neighbor 10.77.0.12 remote-as 65000
    update-source loopback0
    address-family l2vpn evpn
      send-community extended
      route-reflector-client
```

#### Juniper Junos
```
set protocols bgp group EVPN-RR type internal
set protocols bgp group EVPN-RR local-address 10.77.0.1
set protocols bgp group EVPN-RR family evpn signaling
set protocols bgp group EVPN-RR cluster 10.77.0.1
set protocols bgp group EVPN-RR neighbor 10.77.0.11
set protocols bgp group EVPN-RR neighbor 10.77.0.12
```

---

### 3.3 Anycast Gateway Configuration

Provides distributed default gateway across leaf switches for optimal traffic flow.

#### Arista EOS
```
ip virtual-router mac-address 00:1c:73:00:00:01

interface Vlan100
  ip address virtual 192.168.100.1/24

interface Vlan102
  ip address virtual 192.168.102.1/24
```

#### Cisco NX-OS
```
fabric forwarding anycast-gateway-mac 0001.0001.0001

interface Vlan100
  ip address 192.168.100.1/24
  fabric forwarding mode anycast-gateway

interface Vlan102
  ip address 192.168.102.1/24
  fabric forwarding mode anycast-gateway
```

---

### 3.4 MPLS Core Router Configuration

#### Cisco IOS-XR
```
router ospf 1
  area 0
    interface Loopback0
    interface GigabitEthernet0/0/0/1
    interface GigabitEthernet0/0/0/2

mpls ldp
  router-id 10.77.0.31
  interface GigabitEthernet0/0/0/1
  interface GigabitEthernet0/0/0/2

vrf CustomerA
  address-family ipv4 unicast
    import route-target 100:1
    export route-target 100:1

router bgp 65000
  bgp router-id 10.77.0.31
  address-family vpnv4 unicast
  !
  vrf CustomerA
    rd 100:1
    address-family ipv4 unicast
      redistribute connected
```

#### Juniper Junos
```
set protocols ospf area 0.0.0.0 interface lo0.0
set protocols ospf area 0.0.0.0 interface ge-0/0/1.0
set protocols ospf area 0.0.0.0 interface ge-0/0/2.0

set protocols ldp interface ge-0/0/1.0
set protocols ldp interface ge-0/0/2.0

set routing-instances CustomerA instance-type vrf
set routing-instances CustomerA interface ge-0/0/3.0
set routing-instances CustomerA route-distinguisher 100:1
set routing-instances CustomerA vrf-target target:100:1
set routing-instances CustomerA protocols bgp group CE type external
```

---

## 4. Advanced Topics

### 4.1 BUM Traffic Handling
**Broadcast, Unknown Unicast, Multicast (BUM)** traffic in EVPN-VXLAN can be handled via:
- **Ingress Replication** (recommended): Source VTEP replicates to each remote VTEP
- **Head-End Replication (HER)**: Similar to ingress replication
- **Multicast Underlay**: Uses underlay multicast (legacy, not recommended)

### 4.2 MAC Mobility
EVPN supports MAC mobility with sequence numbers in Type 2 routes:
- Detects when a MAC moves between VTEPs
- Sequence number increments with each move
- Prevents loops and ensures consistent forwarding

### 4.3 Route Target Design
**Best Practices**:
- Use unique RD per device: `<loopback>:<vni>`
- Use consistent RT across fabric: `<ASN>:<vni>`
- For L3 VPN: `<ASN>:<vrf-id>`

### 4.4 EVPN Multi-homing (ESI)
Enables active-active connectivity to dual-homed devices:
- Ethernet Segment Identifier (ESI) identifies the multi-homed segment
- All-Active mode for L2 load balancing
- Single-Active mode for compatibility

---

## 5. Packet Flow Explanations

### 5.1 VXLAN Packet Encapsulation
```
[Original Ethernet Frame]
  Destination MAC | Source MAC | EtherType | Payload | FCS

[After VXLAN Encapsulation]
  Outer Ethernet Header
  Outer IP Header (Source: Local VTEP, Dest: Remote VTEP)
  Outer UDP Header (Dest Port: 4789)
  VXLAN Header (VNI: 10100)
  Inner Ethernet Frame (Original)
```

### 5.2 EVPN MAC/IP Learning Flow
1. Host sends packet to Leaf01
2. Leaf01 learns MAC/IP locally
3. Leaf01 advertises Type 2 route to Spines via BGP EVPN
4. Spines reflect to all other Leafs
5. Remote Leafs install MAC/IP in forwarding table with remote VTEP
6. Subsequent traffic flows directly between VTEPs

For detailed end-to-end walkthroughs, see `topology.md` and `vxlan_topology.md`.

---

## 6. Control/Data Plane Details
- **Control plane**: OSPF (underlay), BGP (EVPN), LDP/SR (MPLS)
- **Data plane**: VXLAN encapsulation, MPLS label switching, IP forwarding
- **Underlay**: Provides IP reachability between VTEPs
- **Overlay**: Carries tenant traffic over tunnels

---

## 7. Validation and Troubleshooting

### 7.1 VXLAN/EVPN Validation

**Verify VTEP status**:
```
# Arista
show vxlan vtep
show vxlan vni

# Cisco NX-OS
show nve peers
show nve vni

# Juniper
show evpn instance
show ethernet-switching vxlan-tunnel-end-point remote
```

**Verify EVPN routes**:
```
# Arista
show bgp evpn route-type mac-ip

# Cisco NX-OS
show bgp l2vpn evpn

# Juniper
show route table bgp.evpn.0
```

**Verify MAC learning**:
```
# Arista
show mac address-table dynamic

# Cisco NX-OS
show l2route evpn mac all

# Juniper
show ethernet-switching table
```

### 7.2 MPLS Validation

**Verify LDP neighbors**:
```
# Cisco IOS-XR
show mpls ldp neighbor

# Juniper
show ldp neighbor
```

**Verify label forwarding**:
```
# Cisco IOS-XR
show mpls forwarding

# Juniper
show route table mpls.0
```

### 7.3 Common Issues

| Issue | Symptoms | Resolution |
|-------|----------|------------|
| BGP session down | No EVPN routes | Check underlay reachability, BGP config |
| No VTEP peering | VNI not established | Verify loopback reachability, NVE interface |
| MAC not learned | No connectivity | Check VLAN-VNI mapping, BGP EVPN address-family |
| Asymmetric routing | Packet drops | Verify anycast gateway config on all leafs |

For detailed troubleshooting workflows, see `documentation/troubleshooting/`.

---

## 8. Testing and Automation

**Note**: This documentation describes what a complete implementation would include:
- Ansible playbooks in `ansible/playbooks/` for automated deployment and validation
- Unit/integration tests in `tests/`
- Python scripts for config generation and validation

---

## 9. Best Practices and Security

### 9.1 Design Best Practices
- **Use /32 loopbacks** for VTEP and BGP peering
- **Enable BFD** for fast failure detection
- **Deploy dual route reflectors** for redundancy
- **Use ECMP** with at least 2 uplinks per leaf
- **Separate control and data plane** security policies

### 9.2 Security Controls
- Enable AAA with TACACS+/RADIUS
- Configure SNMP v3 (never v1/v2c in production)
- Deploy logging to centralized syslog server
- Use NTP with authentication
- Enable SSH with key-based authentication only
- Apply control plane policing (CoPP)
- Implement ACLs at security boundaries
- Use VRFs for traffic segmentation

### 9.3 Scalability Guidelines
- **Maximum VNIs per fabric**: 10,000 (vendor dependent)
- **Maximum MAC addresses per VNI**: 1,000-10,000
- **BGP EVPN sessions**: Use route reflectors beyond 10 leafs
- **ECMP paths**: 4-16 paths typical

---

## 10. Glossary and References

### 10.1 Terminology
- **VXLAN**: Virtual Extensible LAN
- **VTEP**: VXLAN Tunnel Endpoint
- **VNI**: VXLAN Network Identifier
- **MPLS**: Multiprotocol Label Switching
- **LDP**: Label Distribution Protocol
- **SR**: Segment Routing
- **EVPN**: Ethernet VPN
- **NLRI**: Network Layer Reachability Information
- **RD**: Route Distinguisher
- **RT**: Route Target
- **ESI**: Ethernet Segment Identifier
- **IMET**: Inclusive Multicast Ethernet Tag
- **BUM**: Broadcast, Unknown unicast, Multicast
- **CoPP**: Control Plane Policing

### 10.2 RFC References
- [RFC 7348](https://datatracker.ietf.org/doc/html/rfc7348) - VXLAN: A Framework for Overlaying Virtualized Layer 2 Networks over Layer 3 Networks
- [RFC 7432](https://datatracker.ietf.org/doc/html/rfc7432) - BGP MPLS-Based Ethernet VPN
- [RFC 8365](https://datatracker.ietf.org/doc/html/rfc8365) - A Network Virtualization Overlay Solution Using Ethernet VPN (EVPN)
- [RFC 4271](https://datatracker.ietf.org/doc/html/rfc4271) - A Border Gateway Protocol 4 (BGP-4)
- [RFC 4364](https://datatracker.ietf.org/doc/html/rfc4364) - BGP/MPLS IP Virtual Private Networks (VPNs)
- [RFC 3107](https://datatracker.ietf.org/doc/html/rfc3107) - Carrying Label Information in BGP-4
- [RFC 5036](https://datatracker.ietf.org/doc/html/rfc5036) - LDP Specification

### 10.3 Vendor Configuration Guides

#### Cisco NX-OS
- **[Cisco Nexus 9000 Series NX-OS VXLAN Configuration Guide, Release 10.5(x)](https://www.cisco.com/c/en/us/td/docs/dcn/nx-os/nexus9000/105x/configuration/vxlan/cisco-nexus-9000-series-nx-os-vxlan-configuration-guide-release-105x.html)**
  - Covers VXLAN BGP EVPN configuration including multi-homing, vPC fabric peering, and ESI configurations
  - Release 10.5(x) updated April 2025

- **[Cisco Nexus 9000 VXLAN BGP EVPN Design and Implementation Guide](https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/cisco-vxlan-bgp-evpn-design-and-implementation-guide.html)**
  - Comprehensive design guide covering:
    - Modular architecture with dedicated device roles (border gateway, border leaf, service leaf)
    - 3-stage and 5-stage CLOS fabric topology
    - Underlay routing protocol selection (OSPF/ISIS recommended)
    - IP unnumbered interfaces to reduce address consumption
    - vPC for endpoint multi-homing
    - Distributed anycast gateway design

**Key Cisco Best Practices**:
- Use dedicated loopback interfaces for VTEP and BGP peering
- Enable ARP suppression across fabric
- Configure auto route target when possible
- Use ECMP for redundancy in underlay
- Separate underlay (IGP) and overlay (BGP EVPN) routing protocols
- Note: Routing protocol adjacencies on Anycast Gateway SVIs are not supported

#### Arista EOS
- **[Arista EOS 4.34.2F - Configuring EVPN](https://www.arista.com/en/um-eos/eos-configuring-evpn)**
  - Latest version from September 2025
  - Covers controller-less BGP EVPN MAC learning using standards-based MP-BGP control plane

- **[Arista EOS 4.34.2F - VXLAN Configuration](https://www.arista.com/en/um-eos/eos-vxlan-configuration)**
  - Detailed VXLAN configuration including designated forwarder election and Ethernet segments

- **[Arista EOS 4.34.2F - EVPN Overview](https://www.arista.com/en/um-eos/eos-evpn-overview)**
  - Comprehensive overview of EVPN implementation supporting both Layer 2 and Layer 3 VPN services

- **[Arista EOS 4.34.2F - Sample Configurations](https://www.arista.com/en/um-eos/eos-sample-configurations)**
  - Practical examples including EVPN peering with spine switches via loopback interfaces

**Key Arista Features**:
- Standards-based BGP EVPN implementation
- Support for EVPN Route-Types 2, 3, and 5
- Integrated with CVP (CloudVision Portal) for automation
- Ingress replication for BUM traffic handling

#### Juniper Junos
- **[Juniper EVPN User Guide](https://www.juniper.net/documentation/us/en/software/junos/evpn/index.html)**
  - Comprehensive guide for configuring and monitoring EVPN-VXLAN, EVPN-MPLS, EVPN-VPWS, and PBB-EVPN

- **[Example: Configure EVPN-VXLAN Centrally-Routed Bridging Fabric](https://www.juniper.net/documentation/us/en/software/junos/evpn/topics/example/evpn-vxlan-mx-qfx-configuring.html)**
  - Detailed CRB (Centrally-Routed Bridging) configuration example
  - Supports MX Series routers, QFX5100, and EX9200 switches
  - Validated on Junos OS 21.3R1.9 (recommended 16.1 or later)

- **[EVPN VXLAN Configuration Overview for QFX Series](https://www.juniper.net/documentation/us/en/software/junos/evpn/topics/concept/evpn-vxlan-configuration-overview.html)**
  - Platform-specific documentation for QFX5100, QFX5110, QFX5200, QFX5210, and EX4600 switches

**Key Juniper Best Practices**:
- Use unique route distinguishers across network devices
- Implement ingress replication for multicast handling
- Configure IRB (Integrated Routing and Bridging) interfaces with virtual gateway addresses
- Use EBGP for underlay, IBGP for overlay
- Implement load balancing policies for ECMP
- Support both single-homed and multi-homed CE device configurations

### 10.4 Additional Standards
- IEEE 802.1Q - VLAN tagging
- IEEE 802.1D - Spanning Tree Protocol
- IEEE 802.3ad - Link Aggregation (LACP)

---

For further details and practical implementations, see the referenced topology diagrams and other documentation files in this repository.
