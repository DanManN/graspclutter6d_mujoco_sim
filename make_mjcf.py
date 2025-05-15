import os
import sys
import xml.etree.ElementTree as ET

import mujoco
import mujoco_viewer

import trimesh
import numpy as np

np.float = float
import open3d as o3d

from tqdm import tqdm
from graspclutter6dAPI import GraspClutter6D
from graspclutter6dAPI.utils.vis import generate_scene_model


def _isArrayLike(obj):
    return hasattr(obj, '__iter__') and hasattr(obj, '__len__')


def loadObjSimple(self, objIds=None):
    '''
    **Function:**

    - load object 3D trimesh of the given obj ids

    **Input:**

    - objIDs: int or list of int of the object ids

    **Output:**

    - a list of trimesh.Trimesh of the models
    '''
    objIds = self.objIds if objIds is None else objIds
    assert _isArrayLike(objIds) or isinstance(
        objIds, int
    ), 'objIds must be an integer or a list/numpy array of integers'
    objIds = objIds if _isArrayLike(objIds) else [objIds]
    models = []
    for i in tqdm(objIds, desc='Loading objects...'):
        plyfile = os.path.join(self.root, 'models_obj_m', 'obj_%06d.obj' % i)
        obj = trimesh.load(plyfile)
        # obj.apply_scale(0.001)
        models.append(obj)
    return models


GraspClutter6D.loadObjSimple = loadObjSimple

if 'GC6D_ROOT' not in os.environ:
    print(
        'Please set the environment variable GC6D_ROOT (e.g. export GC6D_ROOT=/path/to/GraspClutter6D)'
    )
    exit(0)
else:
    gc6d_root = os.environ['GC6D_ROOT']

if len(sys.argv) == 2:
    sys.argv.append('template_shelf.xml')
if len(sys.argv) < 3:
    print(
        'Usage: python make_mjcf.py <sceneId> <template_mjcf_xml_file>\n'
        'Example: python make_mjcf.py 1 template_shelf.xml'
    )
    exit(0)

sceneId = int(sys.argv[1])
annId = 3  # 1~13
camera = 'realsense-d435'  # 'realsense-d415', 'realsense-d435', 'azure-kinect', 'zivid'
scene_name = str(sceneId).zfill(6)

# initialize a GraspNet instance
g = GraspClutter6D(gc6d_root, camera, split='train')

models, objs, poses = generate_scene_model(
    gc6d_root,
    scene_name=scene_name,
    anno_idx=annId,
    return_poses=True,
    camera=camera,
    align=True,
)
print(objs, len(objs))

scene_cloud = o3d.geometry.PointCloud()
for pcd in models:
    scene_cloud += pcd

# 2. Compute the axis‐aligned bounding box
scene_bbox = scene_cloud.get_axis_aligned_bounding_box()

# center = [1.7, 0, 1.6]
# print(dir(scene_bbox))

# Center of surface - offset
center_of_surface = np.array([1.15, 0, 1.14]) 
surface_offset = np.array([0.1, 0, 0])
object_offset = 0.5 * (scene_bbox.min_bound + scene_bbox.max_bound)

center = center_of_surface - surface_offset
center -= object_offset

print(scene_bbox)
### TODO: get bounding box and place objects in a consistent place within the scene
o3d.visualization.draw_geometries(models)
meshes = g.loadObjSimple(objIds=objs)
# scene = trimesh.scene.Scene()
# for mesh, pose in zip(meshes, poses):
#     # mesh.apply_transform(pose)
#     scene.add_geometry(mesh, transform=pose)
# scene.show()

root = ET.parse(sys.argv[2])

com = root.findall('.//compiler')

if len(com) == 0:
    com = ET.SubElement(root, 'compiler')
else:
    # There should only be one compiler
    com = com[0]

com.set('meshdir', gc6d_root)
com.set('texturedir', gc6d_root)

asset = root.findall('.//asset')[0]
worldbody = root.findall('.//worldbody')[0]

repeats = {}
for obj, pose in zip(objs, poses):
    object_name = f"obj_{obj:06d}"
    repeats[object_name] = repeats.get(object_name, -1) + 1
    resource_name = f"{object_name}_{repeats[object_name]}"
    prefix = f'models_obj_m/{object_name}'

    # new_frame = trimesh.transformations.rotation_matrix(np.pi/2, [0, 0, 1])
    new_frame = np.eye(4)
    new_frame[:3, 3] = center
    pose = np.dot(new_frame, pose)

    position = pose[:3, 3]
    quaternion = trimesh.transformations.quaternion_from_matrix(pose)

    obj_xml = ET.parse(f'{gc6d_root}/{prefix}/{object_name}.xml')
    obj_asset = obj_xml.findall('.//asset')[0]
    obj_body = obj_xml.findall('.//body')[0]

    for entry in obj_asset:
        if entry.tag == 'texture':
            tex = ET.SubElement(
                asset, 'texture', {
                    'name': f'{resource_name}_tex',
                    'type': '2d',
                    'file': f'{prefix}/{entry.get("file")}',
                }
            )
        elif entry.tag == 'material':
            mat = ET.SubElement(
                asset, 'material', {
                    'name': f'{resource_name}_mat',
                    'texture': f"{resource_name}_tex",
                    'specular': entry.get('specular', '0.5'),
                    'shininess': entry.get('shininess', '0.5'),
                }
            )
        elif entry.tag == 'mesh':
            filename = entry.get('file')
            if filename.count('collision') == 0:
                mesh_name = 'vis'
            else:
                mesh_name = filename.split('.')[0]
            mesh = ET.SubElement(
                asset,
                'mesh',
                {
                    'name': f'{resource_name}_{mesh_name}',
                    'file': f"{prefix}/{filename}",
                    # 'scale': '0.001 0.001 0.001',
                }
            )

    ## Object body
    body = ET.SubElement(
        worldbody, 'body', {
            'name':
            f"{resource_name}",
            'pos':
            f"{position[0]} {position[1]} {position[2]}",
            'quat':
            f"{quaternion[0]} {quaternion[1]} {quaternion[2]} {quaternion[3]}",
        }
    )

    ## Free joint
    joint = ET.SubElement(
        body, 'joint', {
            'name': f"{resource_name}_joint",
            'type': 'free',
            'limited': 'false',
            'actuatorfrclimited': 'false',
        }
    )

    for entry in obj_body:
        if entry.get('class') == 'visual':
            geom = ET.SubElement(
                body, 'geom', {
                    'name': f'{resource_name}_geom',
                    'type': 'mesh',
                    'contype': '0',
                    'conaffinity': '0',
                    'group': '1',
                    'mesh': f'{resource_name}_vis',
                }
            )
            if entry.get('material') is not None:
                geom.set('material', f'{resource_name}_mat')
        else:
            geom = ET.SubElement(
                body,
                'geom',
                {
                    # 'name': f'{resource_name}_geom',
                    'type': 'mesh',
                    'contype': '3',
                    'conaffinity': '3',
                    'group': '3',
                    'rgba': entry.get('rgba'),
                    'mesh': f'{resource_name}_{entry.get("mesh")}',
                }
            )

# compile to test
curdir = os.path.abspath(os.path.curdir)
string = ET.tostring(root.getroot()).decode().replace('models/rs_table', curdir)
# print(string)
model = mujoco.MjModel.from_xml_string(string)
data = mujoco.MjData(model)
viewer = mujoco_viewer.MujocoViewer(model, data, mode='window')
while viewer.is_alive:
    mujoco.mj_step(model, data)
    viewer.render()

# Save the modified MJCF XML
ET.indent(root)
root.write(f'scenes/scene{sceneId}.xml')
