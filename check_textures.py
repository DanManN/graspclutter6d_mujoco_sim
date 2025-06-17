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


def key_press(self, symbol, modifiers):
    global objname
    print(f"Key: {symbol}")
    if symbol == 102:
        with open('to_fix.txt', 'a') as f:
            f.write(f'{objname}\n')
    else:
        self.close()


SceneViewer.on_key_release = key_press

meshes = g.loadObjTrimesh([x for x in range(1, 201)])
for objid, mesh0 in enumerate(meshes, start=1):
    objname = 'obj_' + str(objid).zfill(6)
    path = gc6d_root + f'/models_obj_m/{objname}/{objname}.obj'
    mesh1 = tm.load(path)
    mesh1.apply_translation(mesh1.bounds[1] - mesh1.bounds[0])

    print(objname)
    scene = tm.Scene([mesh0, mesh1])
    SceneViewer(scene)
