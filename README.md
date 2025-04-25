# Install Requirements
1. Download the [graspclutter6d datasethttps](https://sites.google.com/view/graspclutter6d/dataset)
2. Set the environment variable GC6D_ROOT (e.g. `export GC6D_ROOT=/path/to/GraspClutter6D`)
3. Install obj2mjcf: `pip install --upgrade obj2mjcf`
4. Parse the obj model files with obj2mjcf: `obj2mjcf --obj-dir $GC6D_ROOT/models_obj_m --decompose --save-mjcf`

# Generate a Scene
1. Set the environment variable GC6D_ROOT (e.g. `export GC6D_ROOT=/path/to/GraspClutter6D`)
2. Run `python make_mjcf.py <sceneId> <template_mjcf_xml_file>` for a sceneId between 0-999 and a template mjcf file as a base for the simluation.
For example: `python make_mjcf.py 2 template_shelf.xml`
3. Use the generated `scene<sceneId>.xml` for your needs.
