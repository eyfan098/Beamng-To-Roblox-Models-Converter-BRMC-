import bpy
import zipfile
import sys
import os

zip_path=sys.argv[-1]

extract="temp"

os.makedirs(extract,exist_ok=True)

with zipfile.ZipFile(zip_path,'r') as z:
    z.extractall(extract)

model=None

for root,dirs,files in os.walk(extract):

    for f in files:

        if f.endswith(".dae") or f.endswith(".obj"):

            model=os.path.join(root,f)

bpy.ops.wm.read_factory_settings(use_empty=True)

if model.endswith(".dae"):
    bpy.ops.wm.collada_import(filepath=model)

if model.endswith(".obj"):
    bpy.ops.import_scene.obj(filepath=model)

bpy.ops.export_scene.fbx(
filepath="model.fbx",
embed_textures=True
)
