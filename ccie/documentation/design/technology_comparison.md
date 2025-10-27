# Technology Comparison Matrix

This document compares when to use VXLAN, MPLS, and EVPN technologies for different use cases in the zwu fabric.

---

## Use Case Comparison Matrix

| Use Case | VXLAN | MPLS | EVPN-VXLAN | EVPN-MPLS | Recommended |
|----------|-------|------|------------|-----------|-------------|
| Data center overlay | [+] Excellent | [-] Not suitable | [+] Excellent | [-] Not suitable | EVPN-VXLAN |
| WAN transport | [-] Not suitable | [+] Excellent | [-] Limited | [+] Excellent | EVPN-MPLS or MPLS L3VPN |
| Multi-tenancy | [+] Good (VNI-based) | [+] Good (VRF-based) | [+] Excellent | [+] Excellent | EVPN-VXLAN (DC), EVPN-MPLS (WAN) |
| L2 extension (DCI) | [+] Good | [~] Possible (VPLS) | [+] Excellent | [+] Excellent | EVPN-VXLAN |
| L3 VPN | [~] Requires EVPN | [+] Excellent | [+] Excellent | [+] Excellent | EVPN Type 5 |
| Traffic engineering | [-] Limited | [+] Excellent (RSVP-TE) | [-] Limited | [+] Excellent | MPLS-TE or SR-MPLS |
| Fast reroute | [~] Depends on underlay | [+] Excellent (FRR) | [~] Depends on underlay | [+] Excellent | MPLS FRR |
| Workload mobility | [+] Excellent | [-] Not suitable | [+] Excellent | [~] Limited | EVPN-VXLAN |
| Service chaining | [~] Possible | [+] Good | [+] Good | [+] Excellent | EVPN or MPLS |
| Inter-AS connectivity | [~] Complex | [+] Excellent (Option A/B/C) | [~] Complex | [+] Excellent | EVPN-MPLS or MPLS L3VPN |
| Scalability (segments) | [+] 16M VNIs | [~] Label space limits | [+] 16M VNIs | [~] Label space limits | EVPN-VXLAN |
| Operational simplicity | [+] Good | [~] Complex | [+] Excellent | [~] Complex | EVPN-VXLAN |
| Hardware requirements | [+] Modern switches | [+] MPLS-capable | [+] Modern switches | [+] MPLS-capable | Depends on deployment |

---

## Detailed Technology Analysis

### VXLAN Standalone
**Best For**: Basic L2 overlay in data centers

**Pros**:
- Simple to deploy
- Uses standard IP underlay
- 16M segments vs 4K VLANs
- Works with commodity hardware

**Cons**:
- Flood-and-learn for MAC addresses (inefficient)
- No built-in multi-homing
- Limited L3 capabilities
- No traffic engineering

**When to Use**:
- Simple L2 extension needs
- Budget constraints (no EVPN control plane needed)
- Small-scale deployments

---

### MPLS (L2VPN/L3VPN)
**Best For**: WAN connectivity and service provider networks

**Pros**:
- Mature, proven technology
- Excellent traffic engineering
- Fast reroute capabilities
- Efficient label switching

**Cons**:
- Complex configuration
- Requires MPLS-capable hardware
- Limited scalability in DC environments
- Steeper learning curve

**When to Use**:
- WAN interconnects
- Service provider networks
- Inter-DC connectivity over WAN
- Traffic engineering requirements

---

### EVPN-VXLAN
**Best For**: Modern data center fabrics

**Pros**:
- BGP-based control plane (no flooding)
- Supports L2 and L3 services
- Active-active multi-homing
- Excellent for workload mobility
- Vendor interoperability

**Cons**:
- Requires BGP knowledge
- More complex than standalone VXLAN
- BGP scaling considerations

**When to Use**:
- Data center overlays
- Multi-tenant environments
- Container/VM workloads
- Cloud infrastructure

---

### EVPN-MPLS
**Best For**: Service provider and large enterprise WANs

**Pros**:
- Combines EVPN control plane with MPLS data plane
- Unified L2/L3 services
- Excellent for WAN and DCI
- Traffic engineering + EVPN benefits

**Cons**:
- Most complex option
- Requires MPLS expertise
- Higher cost hardware

**When to Use**:
- Service provider networks
- Large-scale WAN deployments
- Inter-AS DCI
- Unified MPLS networks

---

## Decision Tree

```
Start: What is your primary use case?
|
+-- Data Center Fabric
|   |
|   +-- Simple L2 extension? --> VXLAN (standalone)
|   |
|   +-- Multi-tenant with L2/L3? --> EVPN-VXLAN
|   |
|   +-- Large scale (>1000 endpoints)? --> EVPN-VXLAN with Route Reflectors
|
+-- WAN / Inter-DC
|   |
|   +-- Need traffic engineering? --> MPLS L3VPN with TE
|   |
|   +-- Service provider network? --> EVPN-MPLS
|   |
|   +-- Simple site-to-site? --> MPLS L3VPN
|
+-- Hybrid (DC + WAN)
    |
    +-- EVPN-VXLAN in DC + EVPN-MPLS for WAN (DCI gateway)
```

---

## Performance Comparison

| Metric | VXLAN | MPLS | EVPN-VXLAN | EVPN-MPLS |
|--------|-------|------|------------|-----------|
| Encapsulation overhead | 50 bytes | 4-20 bytes | 50 bytes | 4-20 bytes |
| Convergence time | Slow (flooding) | Fast (FRR) | Fast (BGP) | Fast (BGP+FRR) |
| Control plane overhead | Low | Medium | Medium-High | High |
| MAC learning | Data plane | Data plane | Control plane | Control plane |
| Forwarding efficiency | Good | Excellent | Good | Excellent |

---

## Deployment Scenarios

### Scenario 1: Greenfield Data Center
**Recommendation**: EVPN-VXLAN
- Modern, scalable
- Good vendor support
- Simplified operations

### Scenario 2: Service Provider Network
**Recommendation**: EVPN-MPLS or MPLS L3VPN
- Traffic engineering required
- Inter-AS connectivity
- Mature tooling

### Scenario 3: Enterprise Multi-Site
**Recommendation**: EVPN-VXLAN (DC) + MPLS L3VPN (WAN)
- Best of both worlds
- DC benefits from VXLAN
- WAN benefits from MPLS

### Scenario 4: Budget-Constrained SMB
**Recommendation**: VXLAN standalone
- Lower complexity
- Commodity hardware
- Simpler operations

---

## Migration Paths

### From Traditional VLAN to EVPN-VXLAN
1. Deploy VXLAN underlay (L3 spine-leaf)
2. Enable VXLAN on leafs
3. Implement BGP EVPN control plane
4. Migrate VLANs to VNIs incrementally

### From MPLS L3VPN to EVPN-MPLS
1. Enable EVPN address-family on PEs
2. Configure EVPN instances
3. Migrate services from L3VPN to EVPN
4. Decommission legacy L3VPN

### From VXLAN to EVPN-VXLAN
1. Deploy BGP infrastructure (route reflectors)
2. Configure BGP EVPN on all VTEPs
3. Enable host-reachability protocol bgp
4. Disable flood-and-learn

---

For implementation details, see `fabric_reference.md` and vendor-specific configuration guides.
