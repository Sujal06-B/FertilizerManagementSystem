import os
import django
import json
from django.core.serializers.json import DjangoJSONEncoder

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product, Order
from django.contrib.auth.models import User

def dump_data():
    data = {
        'products': list(Product.objects.values()),
        'orders': list(Order.objects.values()),
        'users': list(User.objects.values('username', 'email', 'is_staff'))
    }
    
    with open('db_data_export.json', 'w') as f:
        json.dump(data, f, cls=DjangoJSONEncoder, indent=4)
    
    print(f"Successfully exported {len(data['products'])} products and {len(data['orders'])} orders to db_data_export.json")

if __name__ == '__main__':
    dump_data()
