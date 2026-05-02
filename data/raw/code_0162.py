import os

def generate_dockerfile():
    dockerfile_content = """
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content.strip())

def generate_kubernetes_manifest():
    k8s_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: your-registry/web-app:latest
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: web-app-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: web-app
"""
    with open("deployment.yaml", "w") as f:
        f.write(k8s_content.strip())

if __name__ == "__main__":
    generate_dockerfile()
    generate_kubernetes_manifest()