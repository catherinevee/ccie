# zwu EVPN-VXLAN Fabric Topology

This diagram illustrates the zwu EVPN-VXLAN fabric topology, including device roles (spine, leaf, border, core), IP addresses, and protocol relationships (OSPF, BGP-EVPN, VXLAN, MPLS). Each router is represented below in ASCII format with technical details about interfaces, VLANs, and traffic flow.

```
Spine Layer:
+-------------------+        +-------------------+
|    Spine01        |        |    Spine02        |
| 10.77.0.1         |        | 10.77.0.2         |
| OSPF/MPLS         |        | OSPF/MPLS         |
| Eth1/1, Eth1/2    |        | Eth1/3, Eth1/4    |
+--------+----------+        +----------+--------+
         | ECMP, IP route: 10.77.0.0/24 |
         |------------------------------|
Leaf Layer:
+--------+----------+        +----------+--------+
|    Leaf01         |        |    Leaf02         |
| 10.77.0.11        |        | 10.77.0.12        |
| BGP-EVPN/VXLAN    |        | BGP-EVPN/VXLAN    |
| VLAN 100, Eth2/1  |        | VLAN 101, Eth2/2  |
+--------+----------+        +----------+--------+
         | MAC route: VNI 5000/5001     |
         |------------------------------|
+--------+----------+        +----------+--------+
|    Leaf03         |        |    Leaf04         |
| 10.77.0.13        |        | 10.77.0.14        |
| BGP-EVPN/VXLAN    |        | BGP-EVPN/VXLAN    |
| VLAN 102, Eth2/3  |        | VLAN 103, Eth2/4  |
+--------+----------+        +----------+--------+
         | MAC route: VNI 5002/5003     |
         |------------------------------|
Border Layer:
+--------+----------+        +----------+--------+
|   Border01        |        |   Border02        |
| 10.77.0.21        |        | 10.77.0.22        |
| MPLS/Interconnect |        | MPLS/Interconnect |
| Eth3/1            |        | Eth3/2            |
+--------+----------+        +----------+--------+
         | MPLS label: 2001/2002        |
         |------------------------------|
Core Layer:
+--------+----------+        +----------+--------+
|   P01             |        |   P02             |
| 10.77.0.31        |        | 10.77.0.32        |
| MPLS L3VPN        |        | MPLS L3VPN        |
| Loopback0         |        | Loopback1         |
+--------+----------+        +----------+--------+
         | VRF: CustomerA/B              |
         |-------------------------------|
+-------------------+
|      PE01         |
|   10.77.0.41      |
| MPLS L3VPN        |
| Loopback0/1       |
+-------------------+
```
