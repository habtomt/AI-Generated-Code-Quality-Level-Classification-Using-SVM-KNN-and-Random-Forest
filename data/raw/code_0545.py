"""
Auto-generated Python code
Scenario : Payment Processing
Prompt   : response_004.txt
Run      : 1
"""

# requirements.txt
Django==4.1.4
django-bootstrap5==3.0.0
python-dotenv==0.20.0

# .env
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=True
ALLOWED_HOSTS=localhost
DATABASE_NAME=YOUR_DB_NAME
DATABASE_USER=YOUR_DB_USER
DATABASE_PASSWORD=YOUR_DB_PASSWORD
DATABASE_HOST=localhost
DATABASE_PORT=5432

# settings.py
import os
from pathlib import Path
import dj_database_url
from django.contrib import messages
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY') or get_random_secret_key()

DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'refunds',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RefundSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'RefundSystem.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f'postgresql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}',
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']

BOOTSTRAP5 = {
    'css_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
    'css_preprocessor': 'None',
    'javascript_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js',
    'javascript_in_head': False,
    'base_url': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/',
}

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

# .gitignore
/refunds/migrations/
/static/

# manage.py
import os
from dotenv import load_dotenv
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    load_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RefundSystem.settings')
    execute_from_command_line(sys.argv)

# refunds/models.py
from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class RefundRequest(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

# refunds/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Payment, RefundRequest
from .forms import RefundRequestForm
from django.contrib.auth.decorators import login_required

@login_required
def request_refund(request):
    if request.method == 'POST':
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            refund_request = form.save(commit=False)
            refund_request.payment = form.cleaned_data['payment']
            refund_request.user = request.user
            refund_request.save()
            messages.success(request, 'Refund request submitted successfully!')
            return redirect('refunds:refund_status')
    else:
        form = RefundRequestForm()
    return render(request, 'refunds/request_refund.html', {'form': form})

@login_required
def manage_refunds(request):
    refunds = RefundRequest.objects.filter(user=request.user)
    return render(request, 'refunds/manage_refunds.html', {'refunds': refunds})

def update_refund_status(request, refund_id):
    refund_request = get_object_or_404(RefundRequest, id=refund_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        refund_request.status = status
        refund_request.save()
        messages.success(request, 'Refund status updated successfully!')
        return redirect('refunds:manage_refunds')
    return render(request, 'refunds/update_refund_status.html', {'refund': refund_request})

# refunds/forms.py
from django import forms
from .models import RefundRequest

class RefundRequestForm(forms.ModelForm):
    
    class Meta:
        model = RefundRequest
        fields = ['payment', 'reason']

# refunds/admin.py
from django.contrib import admin
from .models import Payment, RefundRequest

admin.site.register(Payment)
admin.site.register(RefundRequest)

# RefundSystem/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('refunds.urls')),
]

# templates/refunds/request_refund.html
{% extends 'base.html' %}

{% block content %}
  <h2>Request a Refund</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Request Refund</button>
  </form>
{% endblock %}

# templates/refunds/manage_refunds.html
{% extends 'base.html' %}

{% block content %}
  <h2>Manage Refunds</h2>
  <table class="table">
    <thead>
      <tr>
        <th>Refund ID</th>
        <th>Payment ID</th>
        <th>Reason</th>
        <th>Status</th>
        <th>Created At</th>
      </tr>
    </thead>
    <tbody>
      {% for refund in refunds %}
        <tr>
          <td>{{ refund.id }}</td>
          <td>{{ refund.payment.id }}</td>
          <td>{{ refund.reason }}</td>
          <td>{{ refund.status }}</td>
          <td>{{ refund.created_at }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}

# templates/refunds/update_refund_status.html
{% extends 'base.html' %}

{% block content %}
  <h2>Update Refund Status</h2>
  <form method="post">
    {% csrf_token %}
    <input type="hidden" name="refund_id" value="{{ refund.id }}">
    <select name="status" class="form-select">
      <option value="Pending" {% if refund.status == 'Pending' %} selected {% endif %}>Pending</option>
      <option value="Approved" {% if refund.status == 'Approved' %} selected {% endif %}>Approved</option>
      <option value="Rejected" {% if refund.status == 'Rejected' %} selected {% endif %}>Rejected</option>
    </select>
    <button type="submit" class="btn btn-primary">Update Status</button>
  </form>
{% endblock %}