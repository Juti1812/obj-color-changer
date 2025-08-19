{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww26420\viewh23640\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import bpy\
import bmesh\
\
target_colors = [\
    (1.0, 1.0, 1.0, 1.0),\
    (0.776, 0.757, 0.737, 1.0),\
    (0.686, 0.686, 0.686, 1.0),\
    (0.529, 0.549, 0.549, 1.0),\
]\
\
color_threshold = 0.01\
new_mat_name = "Metalik_Gri"\
\
obj = bpy.context.active_object\
mesh = obj.data\
\
if new_mat_name in bpy.data.materials:\
    new_mat = bpy.data.materials[new_mat_name]\
else:\
    new_mat = bpy.data.materials.new(name=new_mat_name)\
    new_mat.use_nodes = True\
    bsdf = new_mat.node_tree.nodes.get("Principled BSDF")\
    bsdf.inputs["Base Color"].default_value = (0.85, 0.85, 0.85, 1.0)\
    bsdf.inputs["Metallic"].default_value = 1.0\
    bsdf.inputs["Roughness"].default_value = 0.25\
\
if new_mat.name not in [slot.name for slot in obj.material_slots]:\
    obj.data.materials.append(new_mat)\
\
new_mat_index = obj.data.materials.find(new_mat.name)\
\
bpy.ops.object.mode_set(mode='EDIT')\
bm = bmesh.from_edit_mesh(mesh)\
bm.faces.ensure_lookup_table()\
\
for face in bm.faces:\
    mat_index = face.material_index\
    mat = obj.material_slots[mat_index].material\
    if mat and mat.use_nodes:\
        bsdf = mat.node_tree.nodes.get("Principled BSDF")\
        if bsdf:\
            base_color = bsdf.inputs["Base Color"].default_value\
            for target_color in target_colors:\
                diff = sum(abs(base_color[i] - target_color[i]) for i in range(4))\
                if diff < color_threshold:\
                    face.material_index = new_mat_index\
                    break\
\
bmesh.update_edit_mesh(mesh)\
bpy.ops.object.mode_set(mode='OBJECT')\
}