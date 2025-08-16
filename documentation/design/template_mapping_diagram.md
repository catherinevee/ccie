# Configuration/Template Mapping Diagram

This diagram maps Jinja2 templates and variable files to device roles and configuration outputs in the zwu fabric.

```
+-------------------+
|  templates/base/  |
+-------------------+
         |
         v
+-------------------+
|  templates/evpn/  |
+-------------------+
         |
         v
+-------------------+
|  templates/mpls/  |
+-------------------+
         |
         v
+-------------------+
|  templates/services/ |
+-------------------+
         |
         v
+-------------------+
|  variables/global_vars.yml |
|  variables/fabric_vars.yml |
|  variables/devices/*.yml   |
+-------------------+
         |
         v
+-------------------+
|  configs/leaf/*.cfg |
|  configs/spine/*.cfg|
|  configs/border/*.cfg|
|  configs/core/*.cfg |
+-------------------+
```
