#!/bin/bash

# Navigate to your repository
cd Django_Tutorials

# Create or update a timestamp file
echo "Last updated: $(date)" > last_updated.txt

# Add the timestamp file
git add last_updated.txt

# Commit changes with a message
git commit -m "changed date of update"

# Push changes to the remote repository
git push origin main
