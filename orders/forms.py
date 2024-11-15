from django import forms
from .models import Order

from .constants import PAYMENT_CHOICES, DELIVERY_CHOICES


class QuickOrderForm(forms.Form):
    name = forms.CharField(max_length=50, label="Имя")
    last_name = forms.CharField(max_length=50, label="Фамилия")
    email = forms.EmailField(label="Эл.почта")
    phone = forms.CharField(max_length=50, label="Телефон")
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Способ оплаты')
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES, label='Способ Доставки')


class OrderForm(forms.ModelForm):
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Способ оплаты')
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES, label='Способ Доставки')
    class Meta:
        model = Order
        exclude = ('name', 'last_name', 'email', 'phone', 'address')