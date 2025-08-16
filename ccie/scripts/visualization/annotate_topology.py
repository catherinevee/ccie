from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Path to the generated topology diagram
img_path = "/mnt/c/Users/cathe/OneDrive/Desktop/github/ccie/ccie/documentation/design/topology.png"
# Output path for the annotated diagram
output_path = "/mnt/c/Users/cathe/OneDrive/Desktop/github/ccie/ccie/documentation/design/topology_annotated.png"

# Topology description text
header = (
    "zwu EVPN-VXLAN Fabric Topology\n"
    "This diagram illustrates the zwu EVPN-VXLAN fabric topology, including device roles (spine, leaf, border, core), IP addresses, and protocol relationships (OSPF, BGP-EVPN, VXLAN, MPLS). Each router is represented with a custom icon."
)

# Load the image
img = Image.open(img_path)

# Set up drawing context
draw = ImageDraw.Draw(img)

# Choose a font (default PIL font)
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

# Wrap the header text
lines = textwrap.wrap(header, width=80)

# Calculate position for the header
x = 20
y = 20
for line in lines:
    draw.text((x, y), line, font=font, fill="black")
    y += font.getsize(line)[1] + 5

# Save the annotated image
img.save(output_path)
print(f"Annotated diagram saved to {output_path}")
