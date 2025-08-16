# zwu VXLAN Data Plane Topology

This diagram illustrates the VXLAN data plane topology for the zwu fabric, showing how a packet is encapsulated, transported, and decapsulated across the network. It highlights VTEPs, VNIs, and the end-to-end packet process from source to destination.

## VXLAN End-to-End Packet Flow Explanation

- HostA (VLAN 100, connected to Leaf01) sends a packet to HostB (VLAN 102, connected to Leaf03).
- Leaf01 acts as a VTEP, encapsulating the packet in VXLAN (VNI 5000) and forwarding it to the IP address of Leaf03's VTEP.
- The packet traverses the underlay network (Spine01/Spine02) using IP routing and ECMP.
- Leaf03 receives the VXLAN packet, decapsulates it, and forwards it to HostB via VLAN 102.
- The process is fully transparent to the endpoints; only the edge switches (Leafs) perform VXLAN encapsulation/decapsulation.

Legend:
--> : Packet flow direction
[VXLAN] : VXLAN encapsulation/decapsulation
[VTEP] : VXLAN Tunnel Endpoint
[VNI] : VXLAN Network Identifier

```
HostA (VLAN 100)
  |
  | Eth2/1
  v
Leaf01 [VTEP]
  |
  | [VXLAN Encapsulation, VNI 5000]
  v
Spine01/Spine02 (Underlay IP, ECMP)
  |
  | [IP Routing]
  v
Leaf03 [VTEP]
  |
  | [VXLAN Decapsulation, VNI 5000]
  v
HostB (VLAN 102)

VXLAN Overlay:
+--------+          +--------+          +--------+
| Leaf01 |<------->| Spine  |<------->| Leaf03 |
| VTEP   |          | Underlay|        | VTEP   |
+--------+          +--------+        +--------+
   | VNI 5000         | IP Routing      | VNI 5000
   |------------------|----------------|--------|

Other Leafs and Borders participate similarly for their respective VNIs and endpoints.
```
