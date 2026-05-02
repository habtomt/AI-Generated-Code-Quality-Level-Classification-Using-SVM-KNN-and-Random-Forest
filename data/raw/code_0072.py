import os
import subprocess

APP_NAME = "ml-api"
IMAGE_NAME = "ml-api:latest"
DEPLOYMENT_FILE = "deployment.yaml"
SERVICE_FILE = "service.yaml"
HPA_FILE = "hpa.yaml"
DOCKERFILE = "Dockerfile"


# -------------------- Dockerfile --------------------
dockerfile_content = """
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py

EXPOSE 8000

CMD ["python", "app.py"]
"""

# -------------------- Requirements --------------------
requirements = """
fastapi
uvicorn
numpy
scikit-learn
"""

# -------------------- FastAPI App --------------------
app_code = """
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LogisticRegression

app = FastAPI()

model = LogisticRegression()
X = np.array([[0,0],[1,1],[1,0],[0,1]])
y = np.array([0,1,1,0])
model.fit(X, y)

class Input(BaseModel):
    features: list[float]

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/predict")
def predict(data: Input):
    x = np.array(data.features).reshape(1, -1)
    pred = model.predict(x)[0]
    return {"prediction": int(pred)}
"""

# -------------------- Kubernetes Deployment --------------------
deployment_yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {APP_NAME}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: {APP_NAME}
  template:
    metadata:
      labels:
        app: {APP_NAME}
    spec:
      containers:
      - name: {APP_NAME}
        image: {IMAGE_NAME}
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
"""

service_yaml = f"""
apiVersion: v1
kind: Service
metadata:
  name: {APP_NAME}-service
spec:
  selector:
    app: {APP_NAME}
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
"""

hpa_yaml = f"""
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {APP_NAME}-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {APP_NAME}
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
"""

def write_file(filename, content):
    with open(filename, "w") as f:
        f.write(content)

def build_container():
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "."], check=False)

def deploy_k8s():
    subprocess.run(["kubectl", "apply", "-f", DEPLOYMENT_FILE], check=False)
    subprocess.run(["kubectl", "apply", "-f", SERVICE_FILE], check=False)
    subprocess.run(["kubectl", "apply", "-f", HPA_FILE], check=False)

def main():
    write_file(DOCKERFILE, dockerfile_content)
    write_file("requirements.txt", requirements)
    write_file("app.py", app_code)
    write_file(DEPLOYMENT_FILE, deployment_yaml)
    write_file(SERVICE_FILE, service_yaml)
    write_file(HPA_FILE, hpa_yaml)

    build_container()
    deploy_k8s()

if __name__ == "__main__":
    main()