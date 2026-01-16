import os
import django
import random
from datetime import timedelta
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventorysystem4.settings')
django.setup()

from django.contrib.auth.models import User
from dashboard.models import Product, Order
from user.models import Profile

def populate():
    # Create Admin User
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Admin user created (admin/admin123)")
    else:
        print("Admin user already exists")

    # Create Staff Users
    staff_names = ['Alice', 'Bob', 'Charlie']
    staff_users = []
    for name in staff_names:
        user, created = User.objects.get_or_create(
            username=name.lower(),
            defaults={'email': f'{name.lower()}@example.com'}
        )
        
        if created:
            user.set_password('staff123')
            user.save()
            print(f"Staff user {user.username} created (password: staff123)")
        
        # Ensure Profile exists
        Profile.objects.get_or_create(
            staff=user, 
            defaults={'address': f'123 {name} St', 'phone': f'555-010{random.randint(1,9)}'}
        )

        staff_users.append(user)

    # Products Data
    products_data = [
        {'name': 'Dell XPS 15', 'category': 'Laptop', 'quantity': 50, 'price': 1500.00},
        {'name': 'MacBook Pro', 'category': 'Laptop', 'quantity': 30, 'price': 2000.00},
        {'name': 'iPhone 14', 'category': 'Phone', 'quantity': 100, 'price': 999.00},
        {'name': 'Samsung Galaxy S23', 'category': 'Phone', 'quantity': 80, 'price': 899.00},
        {'name': 'iPad Air', 'category': 'Tablet', 'quantity': 40, 'price': 600.00},
        {'name': 'Sony Headphones', 'category': 'Electronics', 'quantity': 60, 'price': 300.00},
        {'name': 'Logitech Mouse', 'category': 'Electronics', 'quantity': 150, 'price': 50.00},
        {'name': 'Office Paper', 'category': 'Stationary', 'quantity': 500, 'price': 10.00},
        {'name': 'Pens (Box)', 'category': 'Stationary', 'quantity': 200, 'price': 5.00},
        {'name': 'Sandwich', 'category': 'Food', 'quantity': 20, 'price': 8.00},
        {'name': 'Apple Watch', 'category': 'Smart Watch', 'quantity': 45, 'price': 400.00},
    ]

    # Create Products
    products_objs = []
    for p_data in products_data:
        product, created = Product.objects.get_or_create(
            name=p_data['name'],
            defaults={
                'category': p_data['category'],
                'quantity': p_data['quantity'],
                'price': p_data['price']
            }
        )
        if created:
            print(f"product {product.name} created")
        products_objs.append(product)

    # Create Orders
    # Create some orders for different products and staff
    for _ in range(20):
        product = random.choice(products_objs)
        staff = random.choice(staff_users)
        qty = random.randint(1, 5)
        
        # Ensure we don't order more than available (logic check, though model doesn't enforce it strictly yet)
        if product.quantity >= qty:
            status = random.choice(['Pending', 'Completed', 'Declined'])
            Order.objects.create(
                product=product,
                staff=staff,
                order_quantity=qty,
                status=status,
                date=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            
            # Simple stock adjustment simulation (optional, but good for realism)
            product.quantity -= qty
            product.save()
            print(f"Order created: {qty} x {product.name} by {staff.username}")

    print("Database populated successfully!")

if __name__ == '__main__':
    populate()
