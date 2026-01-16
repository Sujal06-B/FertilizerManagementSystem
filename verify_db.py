
import os
import django
from django.conf import settings

# Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product, Order

print(f"DB Path: {settings.DATABASES['default']['NAME']}")
print(f"File Exists: {os.path.exists(settings.DATABASES['default']['NAME'])}")
print(f"Products: {Product.objects.count()}")
print(f"Orders: {Order.objects.count()}")
print("--- Verification End ---")
