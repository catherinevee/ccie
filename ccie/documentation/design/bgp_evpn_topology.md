# zwu BGP-EVPN Control Plane Topology

This diagram illustrates the BGP-EVPN control plane topology for the zwu fabric, showing how BGP sessions and EVPN route advertisements are established between devices. It highlights route reflectors, peerings, and the flow of EVPN NLRI (Network Layer Reachability Information).

## BGP-EVPN Control Plane Flow Explanation

- Each Leaf and Border device establishes iBGP sessions with the Spine routers, which act as route reflectors.
- EVPN NLRI (MAC/IP routes, VTEP information) is advertised from Leaf/Border devices to the Spines, then reflected to all other peers.
- Border devices also establish eBGP sessions for external EVPN or inter-AS connectivity.
- Control plane redundancy is achieved via multiple route reflectors (Spine01, Spine02).

Example EVPN MAC/IP Advertisement:
Leaf01 advertises MAC/IP reachability for a connected endpoint to Spine01/Spine02 via iBGP EVPN. The Spines reflect this information to all other Leafs and Borders, enabling seamless VXLAN overlay connectivity.

Legend:
--> : BGP session direction
[iBGP] : Internal BGP session
[eBGP] : External BGP session
[EVPN] : EVPN NLRI advertisement

```
Spine Layer (Route Reflectors):
+-------------------+        +-------------------+
|    Spine01        |        |    Spine02        |
| 10.77.0.1         |        | 10.77.0.2         |
| iBGP RR           |        | iBGP RR           |
+--------+----------+        +----------+--------+
         ^                          ^
         |                          |
         |                          |
Leaf/Border Layer:
+--------+----------+        +----------+--------+
|    Leaf01         |        |    Leaf02         |
| 10.77.0.11        |        | 10.77.0.12        |
| iBGP [EVPN]       |        | iBGP [EVPN]       |
+--------+----------+        +----------+--------+
         ^                          ^
         |                          |
+--------+----------+        +----------+--------+
|    Leaf03         |        |    Leaf04         |
| 10.77.0.13        |        | 10.77.0.14        |
| iBGP [EVPN]       |        | iBGP [EVPN]       |
+--------+----------+        +----------+--------+
         ^                          ^
         |                          |
+--------+----------+        +----------+--------+
|   Border01        |        |   Border02        |
| 10.77.0.21        |        | 10.77.0.22        |
| iBGP [EVPN]       |        | iBGP [EVPN]       |
| eBGP (DCI/InterAS)|        | eBGP (DCI/InterAS)|
+--------+----------+        +----------+--------+
         ^                          ^
         |                          |
         |--------------------------|
         | EVPN NLRI reflected to all peers
```
