import os

def create_ccie_project_structure(base_path):
    folders = [
        "MPLS",
        "EVPN",
        "L2VPN",
        "VXLAN"
    ]
    platforms = [
        "Cisco_IOS_XR",
        "Juniper_Junos",
        "Arista_EOS"
    ]
    for folder in folders:
        for platform in platforms:
            path = os.path.join(base_path, folder, platform)
            os.makedirs(path, exist_ok=True)
            config_file = os.path.join(path, "production_config.txt")
            with open(config_file, "w") as f:
                f.write(f"# {folder} production-ready configuration for {platform}\n")
                f.write("# Insert validated configuration here\n")

if __name__ == "__main__":
    create_ccie_project_structure("CCIE_Project")