import os

import numpy as np

np.float = float

import trimesh as tm
from trimesh.viewer.windowed import SceneViewer

from graspclutter6dAPI import GraspClutter6D

# GraspClutter6D example for visualization.

if 'GC6D_ROOT' not in os.environ:
    print(
        'Please set the environment variable GC6D_ROOT (e.g. export GC6D_ROOT=/path/to/GraspClutter6D)'
    )
    exit(0)
else:
    gc6d_root = os.environ['GC6D_ROOT']

annId = 3  # 1~13
camera = 'realsense-d435'  # 'realsense-d415', 'realsense-d435', 'azure-kinect', 'zivid'

# initialize a GraspNet instance
g = GraspClutter6D(gc6d_root, camera, split='train')

with open('to_fix.txt', 'r') as f:
    obj_names = f.read().splitlines()

for objname in obj_names:

    # with open(gc6d_root + f'/models_obj/{objname}.obj.mtl', 'r') as f:
    #     lines = f.read().splitlines()
    #     print(lines)
    #     print(objname)
    # input('Press Enter to continue...')
    # continue

    path = gc6d_root + f'/models_obj/{objname}.obj'
    mesh_big = tm.load(path)
    mesh_big.apply_scale(0.001)

    path = gc6d_root + f'/models_obj_m/{objname}/{objname}.obj'
    mesh1 = tm.load(path)
    mesh1.apply_translation(mesh1.bounds[1] - mesh1.bounds[0])

    mesh_big.export(path)
    mesh0 = tm.load(path)
    mesh0.apply_translation(mesh1.bounds[0] - mesh1.bounds[1])

    print(objname)
    scene = tm.Scene([mesh_big, mesh1, mesh0])
    SceneViewer(scene)
