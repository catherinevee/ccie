# Change Management and Versioning Diagram

This diagram shows how configuration changes are tracked, tested, and rolled back in the zwu fabric.

```
+-------------------+
|  Git Repository   |
+-------------------+
         |
         v
+-------------------+
|  Pull Request     |
+-------------------+
         |
         v
+-------------------+
|  CI/CD Pipeline   |
+-------------------+
         |
         v
+-------------------+
|  Automated Tests  |
+-------------------+
         |
         v
+-------------------+
|  Deployment       |
+-------------------+
         |
         v
+-------------------+
|  Rollback (if needed) |
+-------------------+
```
