# Automation Workflow Diagram

This diagram shows how Ansible playbooks, Python scripts, and CI/CD pipelines interact for deployment, validation, and rollback in the zwu fabric.

```
+-------------------+
|  Ansible Playbooks|
+-------------------+
         |
         v
+-------------------+
|  Python Scripts   |
+-------------------+
         |
         v
+-------------------+
|  CI/CD Pipeline   |
|  (.github/workflows/ci.yml) |
+-------------------+
         |
         v
+-------------------+
|  Device Deployment|
+-------------------+
         |
         v
+-------------------+
|  Validation/Tests |
+-------------------+
         |
         v
+-------------------+
|  Rollback Scripts |
+-------------------+
```
