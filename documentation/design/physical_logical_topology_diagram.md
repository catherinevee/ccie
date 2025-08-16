# Physical and Logical Topology Diagram

This diagram shows both physical cabling layouts and logical overlays (VLAN, VNI, VRF assignments) in the zwu fabric.

```
Physical:
Leaf01 -- Spine01
Leaf01 -- Spine02
Leaf02 -- Spine01
Leaf02 -- Spine02
Border01 -- CoreP01
Border02 -- CoreP02

Logical:
Leaf01: VLAN 100, VNI 5000, VRF CustomerA
Leaf02: VLAN 101, VNI 5001, VRF CustomerB
Border01: VRF External, MPLS PE
Spine01/Spine02: OSPF, BGP-EVPN, MPLS Core
```
