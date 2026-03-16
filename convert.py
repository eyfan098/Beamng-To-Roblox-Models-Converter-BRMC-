import bpy
import zipfile
import sys
import os

zip_path = sys.argv[-1]
extract = "temp"

os.makedirs(extract, exist_ok=True)

# Extracting ZIP
with zipfile.ZipFile(zip_path,'r') as z:
    files = z.namelist()
    total_files = len(files)
    for i, f in enumerate(files, 1):
        z.extract(f, extract)
        print(f"EXTRACT_FILE:{i}:{total_files}", flush=True)  # per-file progress

# Optional: convert DDS -> PNG textures here
textures = []
for root, dirs, files in os.walk(extract):
    for f in files:
        if f.lower().endswith(".dds"):
            textures.append(os.path.join(root,f))

for t in textures:
    print("CONVERT_TEXTURE", flush=True)
    # conversion code if needed

# Find model
model = None
for root, dirs, files in os.walk(extract):
    for f in files:
        if f.endswith(".dae") or f.endswith(".obj"):
            model = os.path.join(root, f)

# Blender import
if model:
    print("IMPORT_MODEL", flush=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if model.endswith(".dae"):
        bpy.ops.wm.collada_import(filepath=model)
    elif model.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=model)

# Export FBX
print("EXPORT_FBX", flush=True)
bpy.ops.export_scene.fbx(
    filepath="model.fbx",
    embed_textures=True
)

print("DONE", flush=True)
