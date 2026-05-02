import os
import numpy as np
import subprocess

# --- 1. The Optimized Edge Inference Engine (edge_inference.py content) ---
edge_script = """
import numpy as np
import onnxruntime as ort
import time

class EdgeInferenceEngine:
    def __init__(self, model_path="model_optimized.onnx"):
        # Select CUDA Execution Provider for GPU; fallback to CPU if unavailable
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        self.session = ort.InferenceSession(model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name

    def infer(self, input_data):
        # input_data: numpy array of shape (N, 4)
        start_time = time.perf_counter()
        
        # Run inference using ONNX Runtime (highly optimized for C++/GPU)
        results = self.session.run(None, {self.input_name: input_data.astype(np.float32)})
        
        latency = (time.perf_counter() - start_time) * 1000
        return results[0], latency

if __name__ == "__main__":
    # Offline dummy data test
    engine = EdgeInferenceEngine()
    dummy_input = np.random.rand(1, 4)
    prediction, ms = engine.infer(dummy_input)
    print(f"Prediction: {prediction} | Latency: {ms:.2f}ms")
"""

# --- 2. Model Optimization Logic (Conversion to ONNX) ---
optimizer_script = """
import torch
import torch.nn as nn
import torch.onnx

class LightweightNet(nn.Module):
    def __init__(self):
        super(LightweightNet, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(4, 8),
            nn.ReLU(),
            nn.Linear(8, 2)
        )

    def forward(self, x):
        return self.fc(x)

def export_optimized_model():
    model = LightweightNet().eval()
    dummy_input = torch.randn(1, 4)
    
    # Export to ONNX format for minimal footprint and hardware acceleration
    torch.onnx.export(
        model, 
        dummy_input, 
        "model_optimized.onnx",
        export_params=True,
        opset_version=12,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )
    print("Optimized ONNX model generated.")

if __name__ == "__main__":
    export_optimized_model()
"""

def generate_edge_package():
    # Save inference script
    with open("edge_inference.py", "w") as f:
        f.write(edge_script.strip())
        
    # Save optimization script
    with open("optimize_model.py", "w") as f:
        f.write(optimizer_script.strip())
    
    # Requirements for edge environment
    with open("requirements_edge.txt", "w") as f:
        f.write("onnxruntime-gpu\\nnumpy\\ntorch\\n")

    print("Edge deployment files generated: edge_inference.py, optimize_model.py, requirements_edge.txt")

if __name__ == "__main__":
    generate_edge_package()