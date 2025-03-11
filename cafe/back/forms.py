from django import forms

from .models import Cafe, MenuItem
from django.core.exceptions import ValidationError


class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда",
        required=True
    )

    class Meta:
        model = Cafe
        fields = ['table_number', 'items']

    def clean(self):
        table_num = self.cleaned_data.get('table_number')
        status = self.cleaned_data.get('status')

        if table_num is not None:
            table = Cafe.objects.filter(table_number=table_num).exclude(status='paid')  # Запрос к бд кафе номер стола или статус

            if table.exists():
                if status in ['pending', 'ready']:  # Обработка ошибки по столику и статусу
                    raise ValidationError(f"Столик {table_num} уже занят, выберите другой")
        return self.cleaned_data


class CafeStatusForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['status']


class MenuUpdateForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда",
        required=True
    )

    class Meta:
        model = Cafe
        fields = ['items']


class MenuForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        label="Меню",
    )

    class Meta:
        model = Cafe
        fields = ['items']
