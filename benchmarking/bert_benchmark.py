import torch
from transformers import BertTokenizer, BertForQuestionAnswering
import time
import psutil
import sys



# Function to select device
def select_device():
    device_type = sys.argv[1]
    if device_type == 'gpu' and torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

device = select_device()

# Load pre-trained BERT model
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForQuestionAnswering.from_pretrained(model_name)
model = model.to(device)

# Prepare input
question = "What is the capital of France?"
context = "The capital of France is Paris."
inputs = tokenizer(question, context, return_tensors='pt')
inputs = inputs.to(device)

# Benchmarking loop
num_iterations = 100
total_time = 0

# Warm-up GPU
for _ in range(10):
    _ = model(**inputs)

# Measure inference time
for _ in range(num_iterations):
    start_time = time.time()
    _ = model(**inputs)
    end_time = time.time()
    total_time += end_time - start_time

# Calculate average inference time
avg_inference_time = total_time / num_iterations
print("Average Inference Time:", avg_inference_time, "seconds")

# Memory usage
gpu_memory_usage = torch.cuda.max_memory_allocated() / 1024**3  # in GB
print("GPU Memory Usage:", gpu_memory_usage, "GB")

# CPU utilization
cpu_utilization = psutil.cpu_percent()
print("CPU Utilization:", cpu_utilization, "%")

# Throughput
throughput = num_iterations / total_time
print("Throughput:", throughput, "inputs/second")
