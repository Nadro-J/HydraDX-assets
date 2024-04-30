#!/bin/bash

# Subdirectory containing .json files
DATA_DIR="./data/assets_held"

# Navigate to the directory containing the script (the root of your repository)
cd "$(dirname "$0")"

# OPTIONAL: Add commands to update .json files in $DATA_DIR before committing
# python your_script.py  # If you have a specific script to run beforehand

# Add changes in the /data directory to git
git add $DATA_DIR

# Check if there are any changes; commit them if there are
if git diff --staged --quiet; then
  echo "No changes to commit."
else
  git commit -m "Automatically update JSON files in /data directory"

  # Push the changes to GitHub
  git push origin main  # Make sure 'main' is your branch name
fi
