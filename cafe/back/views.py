from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Cafe
from .forms import OrderForm


def order_list(request):  # Список заказов
    query = request.GET.get('q')
    orders = Cafe.objects.all()

    if query:
        orders = orders.filter(
            Q(table_number__icontains=query) | Q(status__icontains=query)
        )

    return render(request, 'order_list.html', {'cafes': orders, 'query': query})  # Передаем результаты и текст ввода


def add_order(request):  # Добавить заказ
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.calculate_total_price()  # Вычисляем сумму заказа
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


def delete_order(request, order_id):  # Удалить заказ
    order = get_object_or_404(Cafe, id=order_id)
    order.delete()
    return redirect('order_list')


def update_status(request, order_id):  # Статус заказа
    order = get_object_or_404(Cafe, id=order_id)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect('order_list')
    return render(request, 'update_status.html', {'order': order})


def total_revenue(request):  # Расчет выручки
    revenue = Cafe.objects.filter(status='paid').aggregate(models.Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'total_revenue.html', {'revenue': revenue})
