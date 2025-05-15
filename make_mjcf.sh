#!/bin/bash

# Check if exactly two arguments are passed
if [ $# -ne 2 ]; then
    echo "Usage: ./script.sh <s|t> <s|u>"
    echo "Args: shelf (s) or table (t), structured (s) or unstructured (u)"
    exit 1
fi

surface_arg=$1
structure_arg=$2

# Interpret surface
if [ "$surface_arg" == "s" ]; then
    echo "Surface: shelf"
    surface="shelf"
elif [ "$surface_arg" == "t" ]; then
    echo "Surface: tabletop"
    surface="tabletop"
else
    echo "Invalid surface type. Use 's' for shelf or 't' for tabletop."
    exit 1
fi

# Interpret structure
if [ "$structure_arg" == "s" ]; then
    echo "Structure: structured"
    structure="structured"
elif [ "$structure_arg" == "u" ]; then
    echo "Structure: unstructured"
    structure="unstructured"
else
    echo "Invalid structure type. Use 's' for structured or 'u' for unstructured."
    exit 1
fi

# Construct scene directory path
category_name="${surface}_${structure}"
scene_parent_dir="./scenes"
scene_dir="${scene_parent_dir}/${category_name}"

# Path to CSV file
category_csv="./${category_name}.csv"

# Check if the CSV file exists
if [ ! -f "$category_csv" ]; then
    echo "CSV file not found: $category_csv"
    exit 1
fi

start_index=0  # For example, start from line 5 (index starts from 0)

# Initialize counter
counter=0

# Read the CSV file
while IFS=, read -r scene_id; do
    # Skip the header line (if any) and empty rows
    if [ "$scene_id" == "scene_id" ] || [ -z "$scene_id" ]; then
        continue
    fi

    # Skip lines before the start_index
    if [ $counter -lt $start_index ]; then
        counter=$((counter + 1))
        continue
    fi

    # Process the scene_id from start_index onward
    echo "$scene_id" "template_${surface}.xml"

    # Run the Python command
    python make_mjcf.py "$scene_id" "template_${surface}.xml" "$category_name"

    # Increment counter
    counter=$((counter + 1))

done < "$category_csv"

echo "Scene directory: $scene_dir"
