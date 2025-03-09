from rest_framework import serializers
from .models import Cafe, MenuItem


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe  # Модель Кафе
        fields = '__all__'  # Включает все поля модели


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem  # Модель Меню
        fields = '__all__'  # Включает все поля модели
