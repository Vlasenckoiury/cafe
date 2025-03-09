from django.contrib import admin
from .models import Cafe, MenuItem


@admin.register(Cafe)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'table_number', 'total_price', 'status')
    list_filter = ('status',)
    search_fields = ('id', 'table_number')


@admin.register(MenuItem)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
