#!/bin/bash

ENV_NAME=datafusionenv  #<--- You can change this

# Check if the environment already exists
if conda info --envs | grep -q "^${ENV_NAME}"; then
    echo "Environment '$ENV_NAME' already exists. Skipping creation."
else
    # Create environment if it doesn't exist
    conda create --name $ENV_NAME python=3.11 -y
fi

# Activate environment
conda activate $ENV_NAME

# Install packages from requirements.txt
pip install -r requirements.txt