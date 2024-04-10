import resnet_benchmark.py as resnet
import opt_benchmarking as opt
import yolo_benchmark as yolo
import sys

device = sys.argv[1]

opt.benchmark(device)