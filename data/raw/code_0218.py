import os
import subprocess

# --- 1. The Core API Code (ml_api_service.py content) ---
api_code = """
import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

app = Flask(__name__)
MODEL_PATH = 'model.joblib'

def init_model():
    if not os.path.exists(MODEL_PATH):
        X, y = make_classification(n_samples=100, n_features=4, random_state=42)
        model = LogisticRegression().fit(X, y)
        joblib.dump(model, MODEL_PATH)
    return joblib.load(MODEL_PATH)

model = init_model()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)['data']
        prediction = model.predict(np.array(data)).tolist()
        return jsonify({'predictions': prediction, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
"""

# --- 2. The Infrastructure Configurations ---
dockerfile_content = """
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask scikit-learn joblib numpy gunicorn
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "ml_api_service:app"]
"""

k8s_manifest = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-api-deploy
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ml-api
  template:
    metadata:
      labels:
        app: ml-api
    spec:
      containers:
      - name: ml-api
        image: ml-api-service:latest
        resources:
          limits:
            cpu: "500m"
          requests:
            cpu: "200m"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-api-deploy
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
"""

def setup_deployment():
    # Writing files to disk
    with open("ml_api_service.py", "w") as f:
        f.write(api_code)
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())
        
    with open("k8s_config.yaml", "w") as f:
        f.write(k8s_manifest.strip())

    print("Deployment files generated: ml_api_service.py, Dockerfile, k8s_config.yaml")

    # Example command to build (requires Docker installed)
    # subprocess.run(["docker", "build", "-t", "ml-api-service:latest", "."], check=True)

if __name__ == "__main__":
    setup_deployment()