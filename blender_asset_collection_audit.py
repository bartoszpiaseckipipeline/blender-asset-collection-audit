import bpy
from datetime import datetime

# --------------------------------
# Blender Asset Collection Audit
#
# Tool for validating Blender asset collection structure and
# generating a readable text report for pipeline verification.
#
# File          : blender_asset_collection_audit.py
# Author        : Bartosz Piasecki
# GitHub        : https://github.com/bartoszpiaseckipipeline
# License       : MIT
#
# Version       : 0.1.0
#
#      0.1.0
#      │ │ └── PATCH (bug fixes)
#      │ └──── MINOR (new features)
#      └────── MAJOR (breaking changes)
#
# Usage:
#
# 1. Select a collection in the Outliner.
# 2. Run the script in Blender's Text Editor.
# 3. A text report will be generated next to your `.blend` file.
# 4. The output file name is based on the selected collection name
#    with the `_outliner_audit` suffix.
#
# Note:
# - The script requires an active collection selection.
#
# --------------------------------


# Store output lines
output = []


def collect_collection_data(collection, indent=0):
    """
    Recursively collect collection and object names
    preserving hierarchy structure.
    """
    output.append("  " * indent + f"[COLLECTION] {collection.name}")

    for obj in collection.objects:
        output.append("  " * (indent + 1) + f"- {obj.name} [{obj.type}]")

    for child in collection.children:
        collect_collection_data(child, indent + 1)


# Get active collection from the current view layer (Outliner selection)
layer_collection = bpy.context.view_layer.active_layer_collection

if layer_collection is None:
    raise RuntimeError("No active collection selected. Please select a collection in the Outliner.")

collection = layer_collection.collection

# Metadata header (production-style)
output.append("# ----------------------------------------")
output.append("# Blender Asset Collection Audit Report")
output.append("# Author        : Bartosz Piasecki")
output.append("# GitHub        : https://github.com/bartoszpiaseckipipeline")
output.append("# License       : MIT")
output.append("# ----------------------------------------")
output.append(f"# Export Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append(f"# Scene         : {bpy.context.scene.name}")
output.append(f"# Collection    : {collection.name}")
output.append(f"# Blend File    : {bpy.data.filepath}")
output.append("# ----------------------------------------\n")

# Notes / Disclaimer
output.append("# Notes:")
output.append("# - This report is generated automatically and may not detect all asset issues.")
output.append("# - Use as a support tool, not a final validation step.")
output.append("# ----------------------------------------\n")

# Collect hierarchy
collect_collection_data(collection)

# Define output file path
filepath = bpy.path.abspath(f"//{collection.name}_outliner_audit.txt")

# Write data to file
with open(filepath, "w", encoding="utf-8") as file:
    file.write("\n".join(output))

print(f"Export completed: {filepath}")
