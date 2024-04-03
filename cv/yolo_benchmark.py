import torch
import time
from torchvision import datasets, transforms
import torchvision

# Function to select device
def select_device():
    device_type = input("Select device (CPU/GPU): ").lower()
    if device_type == 'gpu' and torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

device = select_device()

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model = model.to(device)

# Prepare data loader (you need to prepare your own dataset)
transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor(),
])

# add dataset where 'test_dataset_path' is
test_dataset = datasets.ImageFolder(root='test_dataset_path', transform=transform)
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False)

# Benchmarking and evaluation
total_time = 0
num_images = 0
correct = 0
total = 0

model.eval()

with torch.no_grad():
    for images, labels in test_loader:
        num_images += 1
        images = images.to(device)
        start_time = time.time()
        outputs = model(images)  # Perform inference
        end_time = time.time()
        total_time += end_time - start_time
        
        # Evaluate accuracy (optional)
        if labels is not None:
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

# Calculate metrics
avg_inference_time = total_time / num_images
accuracy = correct / total if total != 0 else None

# Print results
print("Average Inference Time per Image:", avg_inference_time, "seconds")
if accuracy is not None:
    print("Accuracy:", accuracy)

# Calculate throughput, latency, and FPS
throughput = num_images / total_time
latency = total_time / num_images
fps = 1 / latency

print("Throughput:", throughput, "images/second")
print("Latency:", latency * 1000, "milliseconds")
print("FPS:", fps)
