from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Value, F
from django.db.models.functions import Coalesce


# Create your views here.



@login_required
def staff(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    workers = User.objects.all()
    context={
        'workers':workers,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request, pk):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    workers = User.objects.get(id=pk) 
    context={
        'workers':workers,
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def product(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    items = Product.objects.all() # USING ORM 
    #items = Product.objects.raw('SELECT * FROM dashboard_product')


    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-product')
    else:
        form = ProductForm()


    context={
        'items':items,
        'form':form,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def product_delete(request, pk):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required
def product_update(request, pk):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form':form,
    }
    return render(request, 'dashboard/product_update.html', context)

@login_required
def order(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    orders = Order.objects.all()

    context = {
        'orders':orders,
    }
    return render(request, 'dashboard/order.html', context)

from django import template

register = template.Library()

@login_required
def total_quantity(products):
    return sum(getattr(product, 'product_quantity') for product in products)

@login_required
def index(request):
    # Redirect non-staff (farmers) to their dashboard
    if not request.user.is_staff:
        return redirect('farmer-orders')

    # Fetch all orders
    orders = Order.objects.all()

    # Fetch all products and annotate them with total sold quantity
    products = Product.objects.annotate(
        total_sold=Coalesce(Sum('order__order_quantity'), Value(0))
    )

    # Find the most and least sold products
    most_sold_product = products.order_by('-total_sold').first()
    least_sold_product = products.order_by('total_sold').first()

    # Handle order form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
            return redirect('dashboard-index')
    else:
        form = OrderForm()

    # Context to pass to the template
    context = {
        'orders': orders,
        'form': form,
        'products': products,
        'most_sold_product': most_sold_product,
        'least_sold_product': least_sold_product,
        'workers_count': User.objects.all().count(),
        'farmers_count': User.objects.filter(is_staff=False).count(),
        'products_count': Product.objects.all().count(),
        'orders_count': Order.objects.all().count(),
    }

    return render(request, 'dashboard/index.html', context)

def landing_page(request):
    return render(request, 'dashboard/landingpage.html')

def login_page(request):
    return render(request, 'login.html')

@login_required
def page1(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    items = Product.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added.')
            return redirect('dashboard-page1')
    else:
        form = ProductForm()

    context = {
        'items': items,
        'form': form,
    }
    return render(request, 'dashboard/page1.html', context)

@login_required
def report(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    orders = Order.objects.all()
    products = Product.objects.annotate(
        total_sold=Coalesce(Sum('order__order_quantity'), Value(0))
    )
    most_sold_product = products.order_by('-total_sold').first()
    least_sold_product = products.order_by('total_sold').first()
    
    context = {
        'orders': orders,
        'products': products,
        'most_sold_product': most_sold_product,
        'least_sold_product': least_sold_product,
        'workers_count': User.objects.all().count(),
        'farmers_count': User.objects.filter(is_staff=False).count(),
        'products_count': Product.objects.all().count(),
        'orders_count': Order.objects.all().count(),
    }
    return render(request, 'dashboard/report.html', context)

# Farmer Views
@login_required
def farmer_dashboard(request):
    return redirect('farmer-orders')

@login_required
def farmer_place_order(request):
    if request.user.is_staff:
        return redirect('dashboard-index')
    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product')
        qty = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)
        Order.objects.create(product=product, staff=request.user, order_quantity=qty, status='Pending')
        messages.success(request, 'Order Placed Successfully')
        return redirect('farmer-orders')
    return render(request, 'dashboard/farmer_place_order.html', {'products': products})

@login_required
def farmer_orders(request):
    if request.user.is_staff:
        return redirect('dashboard-index')
    orders = Order.objects.filter(staff=request.user).order_by('-date')
    return render(request, 'dashboard/farmer_orders.html', {'orders': orders})

# Admin Orders View
@login_required
def admin_orders(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    orders = Order.objects.all().order_by('-date')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = Order.objects.get(id=order_id)
        if action == 'accept':
            if order.product.quantity >= order.order_quantity:
                order.product.quantity -= order.order_quantity
                order.product.save()
                order.status = 'Accepted'
                order.save()
                messages.success(request, 'Order Accepted')
            else:
                messages.error(request, 'Insufficient Stock')
        elif action == 'deny':
            order.status = 'Denied'
            order.save()
            messages.info(request, 'Order Denied')
        return redirect('dashboard-admin-orders')
    return render(request, 'dashboard/admin_orders.html', {'orders': orders})

@login_required
def stock_report(request):
    if not request.user.is_staff:
        return redirect('farmer-dashboard')
    # Total Stock Received = Sum of all current product quantities (Simplification)
    # Total Sold = Sum of order quantities where status is Accepted
    # Note: "Total Stock Received" usually means Current + Sold.
    products = Product.objects.all()
    total_stock_current = products.aggregate(Sum('quantity'))['quantity__sum'] or 0
    
    sold_orders = Order.objects.filter(status='Accepted')
    total_sold = sold_orders.aggregate(Sum('order_quantity'))['order_quantity__sum'] or 0
    
    total_received = total_stock_current + total_sold
    
    # Calculate Total Inventory Stock Price (Sum of Quantity * Price for all products)
    total_inventory_value = products.aggregate(total_value=Sum(F('quantity') * F('price')))['total_value'] or 0

    context = {
        'total_received': total_received,
        'total_sold': total_sold,
        'products': products,
        'total_inventory_value': total_inventory_value,
    }
    return render(request, 'dashboard/stock_report.html', context)