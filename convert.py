import bpy
import zipfile
import sys
import os

zip_path = sys.argv[-1]
extract = "temp"

os.makedirs(extract, exist_ok=True)

print("Step 1: Extracting ZIP...")
with zipfile.ZipFile(zip_path,'r') as z:
    z.extractall(extract)

model = None
for root, dirs, files in os.walk(extract):
    for f in files:
        if f.endswith(".dae") or f.endswith(".obj"):
            model = os.path.join(root, f)

bpy.ops.wm.read_factory_settings(use_empty=True)

if model.endswith(".dae"):
    print("Step 2: Importing model...")
    bpy.ops.wm.collada_import(filepath=model)
elif model.endswith(".obj"):
    print("Step 2: Importing model...")
    bpy.ops.import_scene.obj(filepath=model)

print("Step 3: Converting textures...")
# Add texture conversion here if needed

print("Step 4: Exporting FBX...")
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    embed_textures=True
)

print("DONE")
