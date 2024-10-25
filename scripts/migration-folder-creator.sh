#!/bin/bash

# Set the base directory (the folder where you want to start searching)
BASE_DIR="$1"

# Check if base directory is provided and exists
if [ -z "$BASE_DIR" ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
elif [ ! -d "$BASE_DIR" ]; then
  echo "Error: Directory '$BASE_DIR' does not exist."
  exit 1
fi

# Loop through all the subdirectories in the base directory
for dir in "$BASE_DIR"/*; do
  # Check if it's a directory
  if [ -d "$dir" ]; then
    # Check if admin.py exists inside this directory
    if [ -f "$dir/admin.py" ]; then
      echo "Found admin.py in $dir"
      
      # Check if migrations directory exists
      if [ -d "$dir/migrations" ]; then
        echo "migrations directory already exists in $dir"
      else
        # Create the migrations directory and the __init__.py file
        echo "Creating migrations directory in $dir"
        mkdir "$dir/migrations"
        touch "$dir/migrations/__init__.py"
        echo "Created migrations/__init__.py in $dir"
      fi
    fi
  fi
done
