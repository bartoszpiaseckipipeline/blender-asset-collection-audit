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
# Version       : 0.2.0
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
# Changelog:
#
# Version       : 0.1.1
# - fix
# Version       : 0.2.0
# - Added readable scale validation
# - Added negative scale detection (SCALE REVERSED!)
#
# --------------------------------


# Store output lines
output = []


def get_scale_status(obj, tolerance=0.0001):
    """
    Returns readable scale status:
    - OK → uniform + applied
    - CHECK SCALE! → non-uniform or not applied
    - SCALE REVERSED! → negative scale detected
    """
    sx, sy, sz = obj.scale

    # Detect negative scale (mirror)
    has_negative = sx < 0 or sy < 0 or sz < 0

    is_uniform = abs(sx - sy) < tolerance and abs(sx - sz) < tolerance
    is_applied = (
        abs(abs(sx) - 1.0) < tolerance and
        abs(abs(sy) - 1.0) < tolerance and
        abs(abs(sz) - 1.0) < tolerance
    )

    if has_negative:
        return "scale --- SCALE REVERSED!"
    elif is_uniform and is_applied:
        return "scale --- OK"
    else:
        return "scale --- CHECK SCALE!"


def collect_collection_data(collection, indent=0):
    """
    Recursively collect collection and object names
    preserving hierarchy structure.
    """
    output.append("  " * indent + f"[COLLECTION] {collection.name}")

    for obj in sorted(collection.objects, key=lambda o: o.name):
        if obj.type == 'MESH':
            scale_status = get_scale_status(obj)
            output.append(
                "  " * (indent + 1) +
                f"- {obj.name} [{obj.type}] {scale_status}"
            )
        else:
            output.append(
                "  " * (indent + 1) +
                f"- {obj.name} [{obj.type}]"
            )

    for child in sorted(collection.children, key=lambda c: c.name):
        collect_collection_data(child, indent + 1)


# Get active collection from the current view layer
layer_collection = bpy.context.view_layer.active_layer_collection

if layer_collection is None:
    raise RuntimeError("No active collection selected. Please select a collection in the Outliner.")

collection = layer_collection.collection

# Metadata header
output.append("# ----------------------------------------")
output.append("# Blender Asset Collection Audit Report")
output.append("# Author        : Bartosz Piasecki")
output.append("# GitHub        : https://github.com/bartoszpiaseckipipeline")
output.append("# License       : MIT")
output.append("# ----------------------------------------")
output.append(f"# Export Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
output.append(f"# Scene         : {bpy.context.scene.name}")
output.append(f"# Collection    : {collection.name}")

# Handle unsaved file
blend_path = bpy.data.filepath if bpy.data.filepath else "UNSAVED"
output.append(f"# Blend File    : {blend_path}")

output.append("# ----------------------------------------\n")

# Notes
output.append("# Notes:")
output.append("# - This report is generated automatically and may not detect all asset issues.")
output.append("# - Scale check:")
output.append("#     OK               → uniform scale and applied (1,1,1)")
output.append("#     CHECK SCALE!     → non-uniform or not applied")
output.append("#     SCALE REVERSED!  → negative scale (mirror)")
output.append("# ----------------------------------------\n")

# Collect hierarchy
collect_collection_data(collection)

# Define output file path
filepath = bpy.path.abspath(f"//{collection.name}_outliner_audit.txt")

# Write data to file
with open(filepath, "w", encoding="utf-8") as file:
    file.write("\n".join(output))

print(f"Export completed: {filepath}")
