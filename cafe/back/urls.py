from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CafeViewSet, MenuViewSet

router = DefaultRouter()

router.register(r'cafe', CafeViewSet, basename='cafeapi')
router.register(r'menu', MenuViewSet, basename='menuapi')

urlpatterns = [
    path('api/', include(router.urls)),  # Включаем маршруты из DefaultRouter
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:cafe_id>/', views.delete_order, name='delete_order'),
    path('update/<int:cafe_id>/', views.update_status, name='update_status'),
    path('revenue/', views.total_revenue, name='total_revenue'),
]
