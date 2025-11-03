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

# OBJ_ID = int(sys.argv[1])  # Change this to visualize different objects

obj_dict = {}
for OBJ_ID in range(1, 201):  # Visualize objects with ID from 1 to 200
    name = 'obj_' + str(OBJ_ID).zfill(6)
    print('Starting object id:', OBJ_ID)
    model, grippers, poses = visObjGrasp(
        gc6d_root,
        OBJ_ID,
        num_grasp=1000,
        th=0.3,
        max_width=0.08,
    )
    print('Finished sampling grasps for', name)
    # print(len(grippers))
    # print(poses[0])
    # tm.Scene([model]+grippers).show()
    obj_dict[name] = poses
    if OBJ_ID % 10 == 0:
        print('Saving intermediate results...')
        np.save('gc6d_grasp_poses.npy', obj_dict)
        print('Finished saving up to obj id:', OBJ_ID)

print('Saving final results...')
np.save('gc6d_grasp_poses.npy', obj_dict)
print('Done!')
