from zoneinfo import available_timezones

import django_filters

from django.db.models import Max
from django.forms import CheckboxInput
from shop.models import Product

# from django.forms import RadioSelect
# available_choices = (
#     (True, "Да",
#      False, "Нет"),
# )

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label="Название")
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label="Мин. цена")
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label="Макс. цена")
    # available = django_filters.BooleanFilter(field_name='available', label="В наличии", widget=RadioSelect(choices=available_choices))
    available = django_filters.BooleanFilter(field_name='available', label="В наличии", widget=CheckboxInput)

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.data.copy()
        max_price = Product.objects.aggregate(Max('price'))['price__max']
        if 'available' not in self.data:
            self.data['available'] = 'on'
        if 'price_min' not in self.data:
            self.data['price_min'] = 0
        if 'price_max' not in self.data:
            self.data['price_max'] = max_price



# class ProductFilter_(django_filters.FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'name': ['icontains'],
#             'price': ['lte', 'gte'],
#             'available': []
#         }
