from django import forms
from .models import Cafe, MenuItem


class OrderForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(
        queryset=MenuItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда",
        required=True
    )

    class Meta:
        model = Cafe
        fields = ['table_number', 'items', 'status']
