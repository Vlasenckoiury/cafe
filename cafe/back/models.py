from django.db import models
from django.utils.translation import gettext_lazy as _


class MenuItem(models.Model):
    name = models.CharField(_("Название"), max_length=255, )
    price = models.DecimalField(_("Цена"), max_digits=10, decimal_places=2)

    class Meta:
        app_label = "back"
        ordering = ('name', 'price')
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Cafe(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]
    TABLE_CHOICES = [(i, f'Стол {i}') for i in range(1, 6)]  # 5 столов

    table_number = models.IntegerField(_("Номер стола"), choices=TABLE_CHOICES, blank=True, null=True)
    items = models.ManyToManyField(MenuItem, verbose_name="Меню")
    total_price = models.DecimalField(_("Общая стоимость заказа"), max_digits=20, decimal_places=2, blank=True, null=True)
    status = models.CharField(_('Статус заказа'), choices=STATUS_CHOICES, default='pending', blank=True, null=True)

    class Meta:
        app_label = "back"
        ordering = ('table_number',)
        verbose_name = 'Кафе'
        verbose_name_plural = 'Кафе'

    def __str__(self):
        return f"Стол {self.table_number}"

    def calculate_total_price(self):
        # Пересчитывает общую стоимость заказа
        self.total_price = sum(item.price for item in self.items.all())
        self.save()
