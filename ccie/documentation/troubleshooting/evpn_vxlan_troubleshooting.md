# EVPN-VXLAN Troubleshooting Guide

This document provides step-by-step troubleshooting workflows for common EVPN-VXLAN fabric issues.

---

## 1. BGP EVPN Session Issues

### Symptom
- BGP EVPN sessions not establishing
- EVPN routes not being exchanged

### Troubleshooting Steps

1. **Verify underlay connectivity**
   ```
   # Arista
   ping 10.77.0.1 source Loopback0

   # Cisco NX-OS
   ping 10.77.0.1 source-interface loopback0

   # Juniper
   ping 10.77.0.1 source 10.77.0.11
   ```

2. **Check BGP neighbor status**
   ```
   # Arista
   show bgp evpn summary
   show bgp evpn neighbors

   # Cisco NX-OS
   show bgp l2vpn evpn summary
   show bgp l2vpn evpn neighbors

   # Juniper
   show bgp summary
   show bgp neighbor 10.77.0.1
   ```

3. **Verify BGP configuration**
   - Check neighbor statements
   - Verify update-source configured (should be Loopback0)
   - Confirm send-community extended is enabled
   - Verify address-family l2vpn evpn is activated

4. **Check for mismatched AS numbers**
   ```
   # Arista
   show run section router bgp

   # Cisco NX-OS
   show run bgp

   # Juniper
   show configuration protocols bgp
   ```

5. **Review logs for BGP errors**
   ```
   # Arista
   show log | include BGP

   # Cisco NX-OS
   show logging logfile | include BGP

   # Juniper
   show log messages | match bgp
   ```

### Common Fixes
- Ensure loopback interfaces are advertised in underlay IGP
- Verify BGP ASN matches on both sides (iBGP requires same ASN)
- Check firewall/ACLs not blocking TCP 179
- Verify route reflector configuration on spines

---

## 2. VTEP Not Establishing

### Symptom
- VNI not showing remote VTEPs
- No VXLAN tunnels formed

### Troubleshooting Steps

1. **Verify NVE interface status**
   ```
   # Arista
   show interface Vxlan1
   show vxlan vtep

   # Cisco NX-OS
   show interface nve1
   show nve peers

   # Juniper
   show interfaces vtep
   ```

2. **Check VTEP source interface reachability**
   ```
   # Arista
   ping vxlan source-interface Loopback1 10.77.0.12

   # Cisco NX-OS
   ping 10.77.0.12 source-interface loopback1

   # Juniper
   ping 10.77.0.12 source 10.77.0.11
   ```

3. **Verify VNI configuration**
   ```
   # Arista
   show vxlan vni
   show vxlan config-sanity

   # Cisco NX-OS
   show nve vni
   show nve internal platform interface nve 1 detail

   # Juniper
   show vlans extensive
   ```

4. **Check for EVPN IMET (Type 3) routes**
   ```
   # Arista
   show bgp evpn route-type imet

   # Cisco NX-OS
   show bgp l2vpn evpn 3

   # Juniper
   show route table bgp.evpn.0 match-prefix "*3:*"
   ```

### Common Fixes
- Verify VLAN-VNI mapping is consistent across fabric
- Ensure NVE/Vxlan interface is administratively up
- Check that ingress-replication is configured
- Verify BGP EVPN is advertising Type 3 routes

---

## 3. MAC Address Not Learning

### Symptom
- End-to-end connectivity fails
- MAC addresses not appearing in forwarding table

### Troubleshooting Steps

1. **Check local MAC learning**
   ```
   # Arista
   show mac address-table
   show mac address-table vlan 100

   # Cisco NX-OS
   show mac address-table
   show mac address-table vlan 100

   # Juniper
   show ethernet-switching table
   show ethernet-switching table vlan VLAN100
   ```

2. **Verify EVPN Type 2 routes**
   ```
   # Arista
   show bgp evpn route-type mac-ip
   show bgp evpn route-type mac-ip vni 10100

   # Cisco NX-OS
   show bgp l2vpn evpn mac
   show bgp l2vpn evpn vni-id 10100

   # Juniper
   show route table bgp.evpn.0 match-prefix "*2:*"
   ```

3. **Check ARP/ND entries**
   ```
   # Arista
   show ip arp vrf default

   # Cisco NX-OS
   show ip arp

   # Juniper
   show arp
   ```

4. **Verify VLAN-VNI mapping**
   ```
   # Arista
   show vxlan vlan

   # Cisco NX-OS
   show vlan
   show nve vni

   # Juniper
   show vlans extensive
   ```

5. **Check if MAC is in suppression/duplicate detection**
   ```
   # Arista
   show mac address-table notification mac-move

   # Cisco NX-OS
   show l2rib internal dup-mac

   # Juniper
   show ethernet-switching mac-learning-log
   ```

### Common Fixes
- Verify hosts are in correct VLAN
- Check VLAN is mapped to VNI on all relevant leafs
- Ensure route-target configuration matches
- Clear duplicate MAC entries if detected

---

## 4. Asymmetric Routing / Packet Drops

### Symptom
- Intermittent connectivity
- Traffic works in one direction but not the other
- Packet drops at gateways

### Troubleshooting Steps

1. **Verify anycast gateway configuration**
   ```
   # Arista
   show ip virtual-router
   show ip interface brief | include Vlan

   # Cisco NX-OS
   show fabric forwarding anycast-gateway-mac
   show interface vlan 100

   # Juniper
   show interfaces irb
   show virtual-gateway-v4 mac-address
   ```

2. **Check routing table consistency**
   ```
   # Arista
   show ip route vrf default

   # Cisco NX-OS
   show ip route

   # Juniper
   show route table inet.0
   ```

3. **Verify EVPN Type 5 routes (for L3 EVPN)**
   ```
   # Arista
   show bgp evpn route-type ip-prefix

   # Cisco NX-OS
   show bgp l2vpn evpn 5

   # Juniper
   show route table bgp.evpn.0 match-prefix "*5:*"
   ```

4. **Check for MTU issues**
   ```
   # Arista
   show interfaces status

   # Cisco NX-OS
   show interface status

   # Juniper
   show interfaces terse
   ```

### Common Fixes
- Ensure anycast gateway MAC and IP are identical on all leafs
- Verify MTU is adequate (typically 9000+ for overlay networks)
- Check that all leafs have consistent VRF/routing configuration
- Verify symmetric IRB configuration for L3 EVPN

---

## 5. Control Plane Issues

### Symptom
- High CPU usage
- Slow convergence
- Route flapping

### Troubleshooting Steps

1. **Check BGP resource utilization**
   ```
   # Arista
   show bgp evpn summary
   show processes top once

   # Cisco NX-OS
   show bgp l2vpn evpn summary
   show system resources

   # Juniper
   show bgp summary
   show system processes extensive
   ```

2. **Monitor for route flapping**
   ```
   # Arista
   show bgp evpn dampening flap-statistics

   # Cisco NX-OS
   show bgp l2vpn evpn flap-statistics

   # Juniper
   show route damping suppressed
   ```

3. **Verify route reflector configuration**
   ```
   # Spine devices
   # Arista
   show bgp evpn summary | include RR

   # Cisco NX-OS
   show bgp l2vpn evpn neighbors | include route-reflector

   # Juniper
   show bgp neighbor | match cluster
   ```

### Common Fixes
- Implement BGP dampening if routes are flapping
- Increase BGP timers if network is unstable
- Verify route reflector clients are correctly configured
- Check for routing loops in underlay

---

## 6. Data Plane Issues

### Symptom
- Control plane working but no data traffic
- Packet loss in data plane

### Troubleshooting Steps

1. **Verify VXLAN encapsulation/decapsulation**
   ```
   # Arista
   show vxlan counters

   # Cisco NX-OS
   show nve ethernet-segment
   show nve internal platform interface nve 1 counters

   # Juniper
   show interfaces vtep statistics
   ```

2. **Check for packet drops**
   ```
   # Arista
   show interfaces counters errors

   # Cisco NX-OS
   show interface counters errors

   # Juniper
   show interfaces extensive | match drops
   ```

3. **Verify hardware programming**
   ```
   # Arista
   show platform trident l2 table 0

   # Cisco NX-OS
   show system internal l2fwder mac

   # Juniper
   show route forwarding-table family bridging
   ```

### Common Fixes
- Check physical link status and errors
- Verify hardware TCAM resources are not exhausted
- Ensure QoS policies are not dropping traffic
- Check for MTU mismatches

---

## 7. Troubleshooting Workflow Summary

```
[Start]
  |
  v
Is BGP EVPN session up? --> NO --> Check underlay connectivity
  |                                   Check BGP configuration
  | YES                               Check ACLs/firewalls
  v
Are VTEPs peering? --> NO --> Check NVE interface status
  |                          Check VTEP source reachability
  | YES                      Verify Type 3 routes
  v
Are MACs learning? --> NO --> Check local MAC table
  |                          Verify VLAN-VNI mapping
  | YES                      Check Type 2 routes
  v
Is traffic flowing? --> NO --> Check anycast gateway
  |                           Verify routing tables
  | YES                       Check MTU
  v
[Working!]
```

---

## 8. Useful Debug Commands

**Use with caution in production!**

```
# Arista
debug bgp evpn keepalives
debug vxlan

# Cisco NX-OS
debug bgp evpn
debug nve

# Juniper
set protocols bgp traceoptions file bgp-debug
set protocols bgp traceoptions flag all
```

---

For additional troubleshooting scenarios and vendor-specific details, refer to vendor documentation and `fabric_reference.md`.
