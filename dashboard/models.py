from django.db import models
from django.contrib.auth.models import User


# Create your models here.
CATEGORY = (
    ('Urea', 'Urea'),
    ('DAP', 'DAP'),
    ('NPK', 'NPK'),
    ('MOP', 'MOP'),
    ('Organic', 'Organic'),
    ('Bio-Fertilizer', 'Bio-Fertilizer'),
    ('Pesticide', 'Pesticide'),
    ('Seeds', 'Seeds'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    company = models.CharField(max_length=100, null=True, default='Gen')
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)
    quantity = models.PositiveBigIntegerField(null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=1.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return f'{self.name}-{self.quantity}'

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveBigIntegerField(null=True)
    status = models.CharField(max_length=50, default='Pending', null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ordered by {self.staff.username}'


