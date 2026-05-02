import torch
import torch.nn as nn
from torch.utils.mobile_optimizer import optimize_for_mobile

# 1. Define a lightweight Neural Network suitable for mobile
class MobileNetModel(nn.Module):
    def __init__(self):
        super(MobileNetModel, self).__init__()
        self.classifier = nn.Sequential(
            nn.Linear(4, 16),
            nn.ReLU(),
            nn.Linear(16, 2),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.classifier(x)

def convert_for_mobile():
    # Initialize and set to evaluation mode
    model = MobileNetModel()
    model.eval()

    # Create dummy input for tracing (matching the input shape)
    example_input = torch.rand(1, 4)

    # 2. Use TorchScript to trace the model for cross-platform compatibility
    traced_script_module = torch.jit.trace(model, example_input)

    # 3. Apply mobile-specific optimizations (quantization, operator fusion)
    optimized_model = optimize_for_mobile(traced_script_module)

    # 4. Save the model in the .ptl format (PyTorch Lite) for Android/iOS
    optimized_model._save_for_lite_interpreter("model_mobile.ptl")
    
    print("Mobile-optimized model saved as: model_mobile.ptl")

# 5. Example of Real-Time Inference logic within the app framework
def mobile_inference_snippet():
    # This block simulates how the mobile app would run the model
    # Load the optimized model
    model_mobile = torch.jit.load("model_mobile.ptl")
    
    # Simulate real-time sensor data input
    real_time_data = torch.tensor([[0.5, -1.2, 0.8, 2.1]])
    
    with torch.no_grad():
        output = model_mobile(real_time_data)
        prediction = torch.argmax(output, dim=1)
        
    print(f"Mobile Prediction: {prediction.item()}")

if __name__ == "__main__":
    convert_for_mobile()
    mobile_inference_snippet()