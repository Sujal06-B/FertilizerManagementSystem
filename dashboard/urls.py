from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.index, name='dashboard-index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>', views.staff_detail, name='dashboard-staff-detail'),
    path('product/', views.product, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product-update'),
    path('order/', views.order, name='dashboard-order'),
    path('page1/', views.page1, name='dashboard-page1'),
    path('report/', views.report, name='dashboard-report'),
    path('staff/orders/', views.admin_orders, name='dashboard-admin-orders'),
    path('staff/stock/', views.stock_report, name='dashboard-stock-report'),
    path('farmer/dashboard/', views.farmer_dashboard, name='farmer-dashboard'),
    path('farmer/place_order/', views.farmer_place_order, name='farmer-place-order'),
    path('farmer/orders/', views.farmer_orders, name='farmer-orders'),
    path('', views.landing_page, name='landing_page'),
]