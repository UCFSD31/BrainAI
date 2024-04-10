#!/bin/bash

# Check if the correct number of arguments is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <cpu/gpu>"
    exit 1
fi

# Store the input argument
device=$1

# Check if the device is either cpu or gpu
if [ "$device" != "cpu" ] && [ "$device" != "gpu" ]; then
    echo "Invalid device. Please provide either 'cpu' or 'gpu'."
    exit 1
fi

# Call the Python script with the input
python benchmarks.py "$device"
