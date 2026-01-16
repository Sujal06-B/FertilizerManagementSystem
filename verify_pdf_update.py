import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product

def verify():
    # Check specific tricky products
    names = ['Krushiudhyog 20.10.10', 'Urea 46.- -', 'G 5', '20/20']
    for name in names:
        try:
            p = Product.objects.get(name=name)
            print(f"Product: {p.name}")
            print(f"  Price: {p.price}")
            print(f"  Weight: {p.weight}")
            print(f"  Quantity: {p.quantity}")
            print(f"  Category: {p.category}")
        except Product.DoesNotExist:
            print(f"Product {name} NOT FOUND")

if __name__ == '__main__':
    verify()
