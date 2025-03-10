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
    total_price = forms.DecimalField(
        label="Итоговая цена",
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})  # Делаем поле только для чтения
    )

    status = forms.CharField(
        initial="В ожидании",
        disabled=True,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), # Делаем поле только для чтения
        label="Статус заказа"
    )

    class Meta:
        model = Cafe
        fields = ['table_number', 'items', 'status']

    def clean(self):
        table_num = self.cleaned_data.get('table_number')
        status = self.cleaned_data.get('status')

        if table_num is not None:
            table = Cafe.objects.filter(table_number=table_num).exclude(status='paid')  # Запрос к бд кафе номер стола или статус

            if table.exists():
                if status in ['pending', 'ready']:  # Обработка ошибки по столику и статусу
                    raise ValidationError(f"Столик {table_num}уже занят, Выберите другой")
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
