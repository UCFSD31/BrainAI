import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
import time

# Function to calculate metrics and print progress
def calculate_metrics_and_progress(model, tokenizer, texts, device, print_every=1000):
    start_time = time.time()
    
    perplexity_scores = []
    i = 0
    for  text in texts:
        tokens = tokenizer.encode(text, return_tensors='pt').to(device)
        with torch.no_grad():
            outputs = model(tokens, labels=tokens)
        loss = outputs.loss
        perplexity = torch.exp(loss)
        perplexity_scores.append(perplexity.item())
        
        # Print progress
        if i % print_every == 0:
            print(f"Processed {i + 1} texts.")
        i += 1
    
    total_time = time.time() - start_time
    avg_perplexity = sum(perplexity_scores) / len(perplexity_scores)
    throughput = len(texts) / total_time
    latency = total_time / len(texts)
    
    return avg_perplexity, throughput, latency

def benchmark(device_type):

    if device_type == 'gpu' and torch.cuda.is_available():
        device = torch.device('cuda')
    else:
        device = torch.device('cpu')

    model_name = "facebook/opt-2.7b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

    # Load dataset
    dataset = load_dataset("wikitext", "wikitext-103-raw-v1")
    eval_dataset = dataset["validation"]



    # Adjust this sample size to match the number of texts you want to evaluate
    text_sample = eval_dataset["text"]
    print(len(text_sample))

    # Calculate metrics and print progress
    avg_perplexity, throughput, latency = calculate_metrics_and_progress(model, tokenizer, text_sample, device)

    # Print final results
    print(f"Average Perplexity: {avg_perplexity}")
    print(f"Throughput: {throughput} texts/second")
    print(f"Latency: {latency} seconds/text")
