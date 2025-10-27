# Deployment Validation Checklists

This document provides comprehensive pre-deployment and post-deployment validation checklists for EVPN-VXLAN and MPLS fabrics.

---

## Pre-Deployment Checklist

### Hardware Validation
- [ ] All devices powered on and accessible
- [ ] Correct hardware models deployed per design
- [ ] Sufficient memory and CPU resources
- [ ] Proper cooling and power redundancy
- [ ] Transceivers installed and operational
- [ ] Cabling physically verified and labeled

### Software Preparation
- [ ] Consistent OS versions across device roles
- [ ] Required feature licenses installed
- [ ] Configuration templates prepared
- [ ] Rollback procedures documented
- [ ] Change window scheduled and approved

### Underlay Preparation
- [ ] Physical interfaces configured
- [ ] Loopback interfaces configured with /32 masks
- [ ] IP addressing scheme documented
- [ ] MTU set appropriately (9000+ recommended)
- [ ] Link aggregation (LACP) configured if needed

---

## EVPN-VXLAN Deployment Checklist

### Phase 1: Underlay Validation
- [ ] All physical links up
   ```
   show interface status
   ```
- [ ] IGP (OSPF/IS-IS) neighbors established
   ```
   show ip ospf neighbor
   ```
- [ ] Loopback reachability verified
   ```
   ping 10.77.0.X source loopback0
   ```
- [ ] ECMP paths operational
   ```
   show ip route 10.77.0.X
   ```
- [ ] BFD enabled (if used)
   ```
   show bfd neighbors
   ```

### Phase 2: BGP EVPN Control Plane
- [ ] BGP sessions established to route reflectors
   ```
   show bgp evpn summary
   ```
- [ ] EVPN address-family activated
   ```
   show bgp l2vpn evpn summary
   ```
- [ ] Route reflector configuration verified on spines
   ```
   show bgp neighbors | include route-reflector
   ```
- [ ] send-community extended enabled
   ```
   show run | section bgp
   ```

### Phase 3: VXLAN Data Plane
- [ ] NVE/Vxlan interface operational
   ```
   show interface nve1
   show interface Vxlan1
   ```
- [ ] VLAN-to-VNI mappings configured
   ```
   show vxlan vni
   show nve vni
   ```
- [ ] VTEP source interface reachable
   ```
   ping vxlan source-interface loopback1 10.77.0.X
   ```
- [ ] Ingress replication configured
   ```
   show vxlan config-sanity
   show nve peers
   ```

### Phase 4: EVPN Route Advertisement
- [ ] Type 3 (IMET) routes advertised
   ```
   show bgp evpn route-type imet
   ```
- [ ] VTEP peers discovered
   ```
   show vxlan vtep
   show nve peers
   ```
- [ ] Route distinguishers unique per device
   ```
   show bgp evpn summary
   ```
- [ ] Route targets consistent across fabric
   ```
   show bgp evpn vni-id 10100
   ```

### Phase 5: MAC/IP Learning
- [ ] Local MAC addresses learned
   ```
   show mac address-table
   ```
- [ ] Type 2 (MAC/IP) routes advertised
   ```
   show bgp evpn route-type mac-ip
   ```
- [ ] Remote MAC addresses installed
   ```
   show mac address-table remote
   ```
- [ ] ARP suppression working (if enabled)
   ```
   show ip arp suppression-cache
   ```

### Phase 6: L3 Gateway (If Applicable)
- [ ] Anycast gateway configured identically on all leafs
   ```
   show ip virtual-router
   show fabric forwarding anycast-gateway-mac
   ```
- [ ] SVI interfaces operational
   ```
   show interface vlan 100
   ```
- [ ] Type 5 (IP Prefix) routes advertised (for L3 EVPN)
   ```
   show bgp evpn route-type ip-prefix
   ```
- [ ] Inter-subnet routing functional
   ```
   ping 192.168.102.1 source 192.168.100.10
   ```

---

## MPLS Deployment Checklist

### Phase 1: MPLS Underlay
- [ ] IGP operational (OSPF/IS-IS)
   ```
   show ip ospf neighbor
   ```
- [ ] MPLS enabled on core interfaces
   ```
   show mpls interfaces
   ```
- [ ] LDP neighbors established
   ```
   show mpls ldp neighbor
   ```
- [ ] Label bindings present
   ```
   show mpls ldp bindings
   ```

### Phase 2: L3VPN Configuration
- [ ] VRFs configured with correct RD/RT
   ```
   show vrf
   show ip vrf detail
   ```
- [ ] MP-BGP sessions established
   ```
   show bgp vpnv4 unicast summary
   ```
- [ ] VPN routes advertised
   ```
   show bgp vpnv4 unicast all
   ```
- [ ] PE-CE routing operational
   ```
   show bgp vpnv4 unicast vrf CustomerA
   ```

---

## Post-Deployment Validation

### Connectivity Tests
- [ ] **Intra-VLAN connectivity**
   - Ping between hosts in same VLAN/VNI
   - Verify MAC learning on both local and remote VTEPs

- [ ] **Inter-VLAN connectivity**
   - Ping between hosts in different VLANs
   - Verify anycast gateway responding

- [ ] **External connectivity**
   - Verify border/edge connectivity to WAN/Internet
   - Test NAT functionality if configured

### Performance Validation
- [ ] Throughput testing
   ```
   iperf3 -c <destination> -t 30
   ```
- [ ] Latency measurements within SLA
   ```
   ping <destination> -c 100
   ```
- [ ] No packet loss observed
   ```
   show interface counters errors
   ```
- [ ] CPU/memory utilization normal
   ```
   show processes cpu
   show system resources
   ```

### Failover Testing
- [ ] Link failure convergence < 1 second (with BFD)
   - Shut down uplink, verify traffic reroutes
- [ ] Node failure handled gracefully
   - Power off spine, verify route reflector failover
- [ ] BGP graceful restart functional (if enabled)
   ```
   show bgp neighbors | include Graceful
   ```

### Security Validation
- [ ] AAA authentication working
- [ ] SNMP v3 accessible
- [ ] Syslog messages received by server
- [ ] NTP synchronized
- [ ] SSH access only (Telnet disabled)
- [ ] Control plane policing active
   ```
   show policy-map control-plane
   ```

### Monitoring Setup
- [ ] SNMP traps configured
- [ ] Syslog forwarding operational
- [ ] NetFlow/sFlow enabled (if required)
- [ ] Network monitoring tool polling devices
- [ ] Alerting thresholds configured

---

## Operational Readiness Checklist

### Documentation
- [ ] As-built diagrams updated
- [ ] IP address spreadsheet current
- [ ] Configuration backups stored
- [ ] Runbooks updated
- [ ] Escalation procedures documented

### Team Readiness
- [ ] NOC team trained on new fabric
- [ ] Troubleshooting procedures reviewed
- [ ] Escalation contacts verified
- [ ] On-call schedule established

### Tools and Access
- [ ] Monitoring dashboards configured
- [ ] SSH jump hosts accessible
- [ ] Configuration management system updated
- [ ] Backup/restore procedures tested

---

## Rollback Readiness

### Before Going Live
- [ ] Configuration backups saved
- [ ] Rollback procedure documented and tested
- [ ] Rollback time window estimated
- [ ] Rollback decision criteria defined
- [ ] Stakeholders notified of rollback plan

---

## Sign-Off Template

```
Deployment: EVPN-VXLAN Fabric - Production Data Center
Date: _______________
Engineer: _______________

Pre-Deployment Checklist:  [ ] Complete
Underlay Validation:        [ ] Complete
BGP EVPN Control Plane:     [ ] Complete
VXLAN Data Plane:           [ ] Complete
EVPN Route Advertisement:   [ ] Complete
MAC/IP Learning:            [ ] Complete
L3 Gateway:                 [ ] Complete (N/A if not applicable)

Connectivity Tests:         [ ] Passed
Performance Validation:     [ ] Passed
Failover Testing:           [ ] Passed
Security Validation:        [ ] Passed
Monitoring Setup:           [ ] Complete

Issues Found: _______________________________________________
___________________________________________________________

Rollback Required:          [ ] Yes  [ ] No
If Yes, Reason: ____________________________________________

Approved for Production:    [ ] Yes  [ ] No

Signatures:
Network Engineer: _______________  Date: _______________
Team Lead:        _______________  Date: _______________
Manager:          _______________  Date: _______________
```

---

For detailed troubleshooting procedures, see `documentation/troubleshooting/evpn_vxlan_troubleshooting.md`.
