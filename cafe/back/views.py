from django.contrib import messages
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Cafe, MenuItem
from .forms import OrderForm, CafeStatusForm, MenuForm
from .serializers import CafeSerializer, MenuSerializer
from rest_framework import viewsets
import requests
from django.shortcuts import render


class CafeViewSet(viewsets.ModelViewSet):  # Представления кафе для drf
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer


class MenuViewSet(viewsets.ModelViewSet): # Представления меню для drf
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer


def order_list(request):  # Список заказов
    query = request.GET.get('q')
    orders = Cafe.objects.all()

    if query:
        orders = orders.filter(
            Q(table_number__icontains=query) | Q(status__icontains=query)  # проверка на колонки на номер стола или статус
        )

    return render(request, 'order_list.html', {'orders': orders, 'query': query})  # Передаем результаты и текст ввода


def add_order(request):  # Добавить заказ
    if request.method == 'POST':
        form = OrderForm(request.POST)
        try:
            order = form.save()
            order.calculate_total_price()  # Высчитывает стоимость
            messages.success(request, "Заказ успешно добавлен!")  # Успешно добавлено
            return redirect('order_list')  # редирект на главную страницу
        except Exception as e:
            messages.error(request, "Ошибка при добавлении заказа.")  # Ловит любые ошибки
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


def delete_order(request, cafe_id):  # Удалить заказ
    try:
        order = get_object_or_404(Cafe, id=cafe_id)
        order.delete()  # удаляет по id заказ
        return redirect('order_list')
    except Exception as e:
        messages.error(request, "Ошибка при удалении заказа.")  # Ловим любые ошибки


def update_status(request, cafe_id):  # Статус заказа
    cafe = get_object_or_404(Cafe, id=cafe_id)
    if request.method == 'POST':
        form = CafeStatusForm(request.POST, instance=cafe)
        if form.is_valid():
            try:
                form.save()  # сохраняем обновленный статус
                return redirect('order_list')  # редирект на главную страницу
            except Exception as e:
                messages.error(request, "Ошибка при изменении статуса.")  # Ловит любые ошибки
        else:
            print("Форма не валидна.")
            messages.error(request, "Ошибка.")
    else:
        form = CafeStatusForm(instance=cafe)  # для гет-запроса создаем форму с текущим статусом
    return render(request, 'update_status.html', {'form': form, 'cafe': cafe})


def menu_update(request, cafe_id):
    cafe = get_object_or_404(Cafe, id=cafe_id)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=cafe)
        if form.is_valid():
            try:
                form.save()  # сохраняем обновленный статус
                return redirect('order_list')  # редирект на главную страницу
            except Exception as e:
                messages.error(request, "Ошибка при изменении меню.")  # Ловит любые ошибки
        else:
            print("Форма не валидна.")
            messages.error(request, "Ошибка.")  # Ловит любые ошибки
    else:
        form = MenuForm(instance=cafe)  # для гет-запроса создаем форму с текущим статусом
    return render(request, 'update_status.html', {'form': form, 'cafe': cafe})


def total_revenue(request):  # Расчет выручки
    try:
        revenue = Cafe.objects.filter(status='paid').aggregate(models.Sum('total_price'))['total_price__sum'] or 0
        return render(request, 'total_revenue.html', {'revenue': revenue})
    except Exception as e:
        messages.error(request, "Ошибка.")  # Ловит любые ошибки

