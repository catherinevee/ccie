# Redundancy and Failover Diagram

This diagram illustrates high availability mechanisms, ECMP paths, route reflector redundancy, and failover scenarios in the zwu fabric.

```
+-------------------+        +-------------------+
|    Spine01 (RR)   |        |    Spine02 (RR)   |
+--------+----------+        +----------+--------+
         | ECMP Path |
         |-----------|
+--------+----------+        +----------+--------+
|    Leaf01         |        |    Leaf02         |
+--------+----------+        +----------+--------+
         |           |
         |-----------|
         v           v
      Border01    Border02

Failover:
- If Spine01 fails, Spine02 continues as route reflector
- ECMP provides path redundancy between Leafs and Spines
- Border devices provide dual-homed external connectivity
```
