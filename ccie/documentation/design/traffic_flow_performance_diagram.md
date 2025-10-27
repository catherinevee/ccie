# Traffic Flow and Performance Diagram

This diagram visualizes typical traffic patterns, bottlenecks, and performance metrics in the zwu fabric.

```
HostA (Leaf01) --> Leaf01 --> Spine01/Spine02 --> Border01 --> WAN

- ECMP used between Leafs and Spines for load balancing
- Monitor interface utilization on Spine/Border
- Bottleneck: Border WAN link
- Performance metrics: Latency, throughput, packet loss
```
