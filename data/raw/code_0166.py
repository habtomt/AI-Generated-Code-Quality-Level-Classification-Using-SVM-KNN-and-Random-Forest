import os

def generate_github_actions_pipeline():
    pipeline_yaml = """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run Tests
      run: pytest tests/

  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Staging
      run: curl -X POST https://api.cloudprovider.com/deploy/staging

  deploy-production:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to Production
      run: curl -X POST https://api.cloudprovider.com/deploy/production
"""
    os.makedirs(".github/workflows", exist_ok=True)
    with open(".github/workflows/main.yml", "w") as f:
        f.write(pipeline_yaml.strip())

if __name__ == "__main__":
    generate_github_actions_pipeline()