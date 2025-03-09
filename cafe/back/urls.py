from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('update/<int:order_id>/', views.update_status, name='update_status'),
    path('revenue/', views.total_revenue, name='total_revenue'),
]
