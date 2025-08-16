# Service Flow Diagram

This diagram shows how L2VPN, L3VPN, multicast, and QoS services traverse the zwu fabric, including ingress/egress points and protocol transitions.

```
HostA (VLAN 100)
  |
  |--[L2VPN]-->
Leaf01 [VTEP]
  |
  |--[VXLAN Encapsulation, VNI 5000]-->
Spine01/Spine02 [MPLS Core]
  |
  |--[L3VPN, VRF CustomerA]-->
Border01 [PE]
  |
  |--[QoS Policy Applied]-->
WAN/External
```

- L2VPN: VLAN extension via VXLAN overlay
- L3VPN: VRF-based routing via MPLS
- Multicast: IGMP/PIM handled at Leaf/Spine
- QoS: Policy applied at Border/PE
