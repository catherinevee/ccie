# Security and Zoning Diagram

This diagram visualizes segmentation (VRFs, ACLs, firewalls), trusted/untrusted zones, and control/data plane separation in the zwu fabric.

```
+-------------------+   Trusted Zone   +-------------------+
|    Leaf Devices   |-----------------|    Spine Devices  |
|   (VRF: Internal) |                 |   (VRF: Internal) |
+-------------------+                 +-------------------+
         |
         | ACL: Permit Internal Traffic
         v
+-------------------+
|   Border Devices  |
| (VRF: External)   |
+-------------------+
         |
         | ACL: Restrict/Log External Traffic
         v
+-------------------+
|   Firewall/NAT    |
+-------------------+
         |
         | Untrusted Zone
         v
+-------------------+
|   Internet/WAN    |
+-------------------+

Control Plane: OSPF, BGP-EVPN, MPLS
Data Plane: VXLAN, MPLS, IP Forwarding
```
