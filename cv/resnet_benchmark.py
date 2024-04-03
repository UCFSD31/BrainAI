import torch
import torchvision.models as models
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import time

# Function to select device
def select_device():
    device_type = input("Select device (CPU/GPU): ").lower()
    if device_type == 'gpu' and torch.cuda.is_available():
        return torch.device('cuda')
    else:
        return torch.device('cpu')

device = select_device()

# Load the ResNet v2 101 model
model = models.resnet101(pretrained=True)
model = model.to(device)  # Move model to selected device
model.eval()  # Set model to evaluation mode

# Load ImageNet validation dataset for benchmarking accuracy
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
val_dataset = datasets.ImageNet(root='./data', split='val', download=True, transform=transform)
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=32, shuffle=False)

# Warm-up GPU
if device.type == 'cuda':
    for _ in range(10):
        _ = model(torch.randn(1, 3, 224, 224).to(device))

# Benchmarking loop
num_iterations = 100
total_time = 0
correct = 0
total = 0

with torch.no_grad():
    for images, labels in val_loader:
        start_time = time.time()
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        end_time = time.time()
        total_time += end_time - start_time
        
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

        if total >= num_iterations * val_loader.batch_size:
            break

# Calculate metrics
accuracy = 100 * correct / total
throughput = num_iterations * val_loader.batch_size / total_time
latency = total_time / total
fps = 1 / latency

print(f"Accuracy: {accuracy:.2f}%")
print(f"Throughput: {throughput:.2f} images/second")
print(f"Latency: {latency * 1000:.2f} ms")
print(f"FPS: {fps:.2f}")
