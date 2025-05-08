import os
import sys

import numpy as np

np.float = float

import cv2
import open3d as o3d

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
sceneId = int(sys.argv[1])  # 0~9999

scene_name = str(sceneId).zfill(6)

# initialize a GraspNet instance
g = GraspClutter6D(gc6d_root, camera, split='train')

pcd = g.loadScenePointCloud(sceneId, camera, annId, align=True)
models = g.loadSceneModel(sceneId, camera, annId, align=True)
o3d.visualization.draw_geometries(models+[pcd])
