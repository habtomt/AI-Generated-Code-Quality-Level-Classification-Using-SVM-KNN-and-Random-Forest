import os
import time
import torch
import torch.nn as nn

MODEL_PATH = "edge_model.pt"


class TinyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(8, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )

    def forward(self, x):
        return self.net(x)


def export_model():
    model = TinyModel().eval()

    dummy_input = torch.randn(1, 8)

    traced = torch.jit.trace(model, dummy_input)
    traced.save(MODEL_PATH)


def load_model(device):
    model = torch.jit.load(MODEL_PATH, map_location=device)
    model.eval()
    return model


def optimize_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def preprocess(input_data, device):
    tensor = torch.tensor(input_data, dtype=torch.float32)
    return tensor.to(device)


def run_inference(model, device, input_data):
    x = preprocess(input_data, device)

    if device.type == "cuda":
        x = x.half()
        model = model.half()

    with torch.inference_mode():
        start = time.time()
        output = model(x)
        end = time.time()

    latency_ms = (end - start) * 1000

    return output.cpu().numpy().tolist(), latency_ms


def benchmark(model, device):
    sample = [0.5] * 8
    outputs, latency = run_inference(model, device, sample)
    print("Output:", outputs)
    print("Latency (ms):", latency)


def main():
    if not os.path.exists(MODEL_PATH):
        export_model()

    device = optimize_device()
    model = load_model(device)

    print(f"Running on device: {device}")

    while True:
        try:
            user_input = input("Enter 8 float values separated by space (or 'exit'): ")

            if user_input.lower() == "exit":
                break

            values = list(map(float, user_input.strip().split()))

            if len(values) != 8:
                print("Please enter exactly 8 values.")
                continue

            output, latency = run_inference(model, device, values)

            print("Prediction:", output)
            print("Latency (ms):", latency)

        except Exception as e:
            print("Error:", str(e))


if __name__ == "__main__":
    main()