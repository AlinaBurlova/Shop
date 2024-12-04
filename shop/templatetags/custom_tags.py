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
