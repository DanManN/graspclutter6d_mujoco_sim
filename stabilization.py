import sys
import os

import csv

def main():
    # Check for required arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <s|t> <s|u>")
        print("Args: shelf (s) or table (t), structured (s) or unstructured (u)")
        sys.exit(1)

    surface_arg = sys.argv[1]
    structure_arg = sys.argv[2]

    # Interpret surface
    if surface_arg == 's':
        print("Surface: shelf")
        surface = "shelf"
    elif surface_arg == 't':
        print("Surface: tabletop")
        surface = "tabletop"
    else:
        print("Invalid surface type. Use 's' for shelf or 't' for tabletop.")
        sys.exit(1)

    # Interpret structure
    if structure_arg == 's':
        print("Structure: structured")
        structure = "structured"
    elif structure_arg == 'u':
        print("Structure: unstructured")
        structure = "unstructured"
    else:
        print("Invalid structure type. Use 's' for structured or 'u' for unstructured.")
        sys.exit(1)

    # Construct scene directory path
    category_name = f"{surface}_{structure}"
    scene_parent_dir = "./scenes"
    scene_dir = os.path.join(scene_parent_dir, category_name)

    category_csv = f"./{category_name}.csv"

    with open(category_csv, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        
        # Optionally skip the header (if it exists)
        header = next(csv_reader)  # Skip the header if there's one
        
        # Iterate through rows
        for row in csv_reader:
            scene_id = int(row[0])

            exec(f"python make_mjcf.py {scene_id} template_{surface}.xml")

    print(f"Scene directory: {scene_dir}")

if __name__ == "__main__":
    main()
