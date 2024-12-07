from django import template

register = template.Library()

@register.filter
def string_value(product_id):
    return str(product_id)

@register.filter
def count_items(cart, product_id):
    return cart.cart[str(product_id)]["quantity"]

@register.filter
def is_even(value):
    return value % 2 == 0

@register.filter
def category_path(path):
    res = 'all'
    if len(path.split('/')) > 4:
        res = path.split('/')[3]
    return res

