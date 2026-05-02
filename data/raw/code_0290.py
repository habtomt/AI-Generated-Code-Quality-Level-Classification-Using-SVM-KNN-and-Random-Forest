import os
import subprocess

# --- 1. Django Production Settings Generator ---
def create_production_settings():
    settings_content = """
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS', '*')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
"""
    with open("pro_settings.py", "w") as f:
        f.write(settings_content)

# --- 2. Dockerfile Generator ---
def create_dockerfile():
    dockerfile_content = """
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]
"""
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

# --- 3. Nginx Configuration & Docker Compose ---
def create_deployment_orchestration():
    docker_compose = """
version: '3.8'

services:
  web:
    build: .
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
    expose:
      - 8000

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  static_volume:
"""
    nginx_conf = """
server {
    listen 80;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /app/staticfiles/;
    }
}
"""
    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)
    with open("nginx.conf", "w") as f:
        f.write(nginx_conf)

# --- Execution ---
if __name__ == "__main__":
    create_production_settings()
    create_dockerfile()
    create_deployment_orchestration()
    
    print("Deployment files generated:")
    print("- pro_settings.py")
    print("- Dockerfile")
    print("- docker-compose.yml")
    print("- nginx.conf")
    
    # Example command to run the deployment
    # subprocess.run(["docker-compose", "up", "--build", "-d"])