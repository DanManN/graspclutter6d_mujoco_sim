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

for sceneId in range(1000):
    scene_name = str(sceneId).zfill(6)

    # initialize a GraspNet instance
    g = GraspClutter6D(gc6d_root, camera, split='train')

    pcd = g.loadScenePointCloud(sceneId, camera, annId, align=True)
    models = g.loadSceneModel(sceneId, camera, annId, align=True)
    # o3d.visualization.draw_geometries(models+[pcd])

    # Create a visualizer with key callback support
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window()

    # Add your geometries (e.g., models and point cloud)
    for geometry in models + [pcd]:
        vis.add_geometry(geometry)

    def on_key_action_tu(vis):
        print(f'Scene: {scene_name} is unstructured tabletop')
        with open('tabletop_unstructured.csv', 'a') as file:
            file.write(scene_name + '\n')
        vis.close()
        return False

    def on_key_action_ts(vis):
        print(f'Scene: {scene_name} is structured tabletop')
        with open('tabletop_structured.csv', 'a') as file:
            file.write(scene_name + '\n')
        vis.close()
        return False

    def on_key_action_su(vis):
        print(f'Scene: {scene_name} is unstructured shelf')
        with open('shelf_unstructured.csv', 'a') as file:
            file.write(scene_name + '\n')
        vis.close()
        return False

    def on_key_action_ss(vis):
        print(f'Scene: {scene_name} is structured shelf')
        with open('shelf_structured.csv', 'a') as file:
            file.write(scene_name + '\n')
        vis.close()
        return False

    # Register a key callback: here, ord('K') is for the 'K' key
    vis.register_key_callback(
        ord('O'), on_key_action_tu
    )  # ./tabletop_unstructured.csv
    vis.register_key_callback(
        ord('P'), on_key_action_ts
    )  # ./tabletop_structured.csv
    vis.register_key_callback(
        ord('['), on_key_action_su
    )  # ./shelf_unstructured.csv
    vis.register_key_callback(
        ord(']'), on_key_action_ss
    )  # ./shelf_structured.csv

    # Run the visualizer
    vis.run()
    vis.destroy_window()
