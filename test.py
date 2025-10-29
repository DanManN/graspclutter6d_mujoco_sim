import os
import sys
import numpy as np

np.float = float
from graspclutter6dAPI import GraspClutter6D
from graspclutter6dAPI.utils.vis import visObjGrasp
import open3d as o3d
import trimesh as tm
import cv2

if 'GC6D_ROOT' not in os.environ:
    print(
        'Please set the environment variable GC6D_ROOT (e.g. export GC6D_ROOT=/path/to/GraspClutter6D)'
    )
    exit(0)
else:
    gc6d_root = os.environ['GC6D_ROOT']

OBJ_ID = int(sys.argv[1])  # Change this to visualize different objects

model, grippers = visObjGrasp(
    gc6d_root,
    OBJ_ID,
    num_grasp=100,
    th=0.3,
    max_width=0.085,
)
tm.Scene([model]+grippers).show()
