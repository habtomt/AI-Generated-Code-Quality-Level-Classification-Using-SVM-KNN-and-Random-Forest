"""
Auto-generated Python code
Scenario : Web Hosting & Deployment
Prompt   : response_001.txt
Run      : 3
"""

# Import necessary libraries for Django, Docker, and Gunicorn
import os
from django.core.wsgi import get_wsgi_application
import docker

# Create a Django settings file for production
class ProductionSettings:
    # Database configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'your_database_host',
            'PORT': '5432',
        }
    }

    # Secret key
    SECRET_KEY = 'your_secret_key'

    # Allowed hosts
    ALLOWED_HOSTS = ['*']

    # Static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    # Templates
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    # Middlewares
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    # Installed apps
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Add your apps here
    ]

    # WSGI application
    WSGI_APPLICATION = 'your_project.wsgi.application'

# Create a Dockerfile for building the application container
with open('Dockerfile', 'w') as f:
    f.write('''FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the command to start the application
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
''')

# Build the Docker image
client = docker.from_env()
image = client.images.build(path='./', tag='your_image_name', dockerfile='Dockerfile')
print(f'Docker image built: {image[0].short_id}')

# Create a Docker compose file for deploying the application
with open('docker-compose.yml', 'w') as f:
    f.write('''version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./your_project:/app
    depends_on:
      - db
    restart: always

  db:
    image: postgres
    environment:
      POSTGRES_USER: your_database_user
      POSTGRES_PASSWORD: your_database_password
      POSTGRES_DB: your_database_name
''')

# Run the application with Docker compose
os.system('docker-compose up -d')