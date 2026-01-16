import os
import django
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from dashboard.models import Product, Order

def test_stats():
    products = Product.objects.annotate(
        total_sold=Coalesce(Sum('order__order_quantity'), Value(0))
    )
    
    print("Testing Product Stats:")
    for p in products[:5]:
        print(f"Product: {p.name}, Total Sold: {p.total_sold}")
        
    most_sold = products.order_by('-total_sold').first()
    if most_sold:
        print(f"Most Sold: {most_sold.name}, Quantity: {most_sold.total_sold}")
    else:
        print("No products found")

if __name__ == '__main__':
    test_stats()
