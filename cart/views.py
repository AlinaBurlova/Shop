import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

from django.views.decorators.csrf import csrf_exempt

from shop.models import Product
from website_shop.settings import CART_SESSION_ID


class Cart:
    def __init__(self, request):
        # получаем текущую сессию
        self.session = request.session
        # получаем текущего пользователя
        self.user = request.user
        # получаем корзину из сессии или создаем новую
        cart = self.session.get(CART_SESSION_ID)
        # создаем новую корзину
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    # сохранение изменений в сессию
    def save(self):
        self.session.modified = True

    # метод помещения товара в корзину
    def add(self, product, quantity=1, override_quantity=False):
        # получаем id товара из ОБЪЕКТА товара
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    # удаление товара из корзины
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # метод подсчета общего количества элементов в корзине
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        # return len(self.cart) - количество товаров в корзмне (без учета кол-ва каждого товара)

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.cart.clear()
        # del self.session[CART_SESSION_ID]
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


def cart_add(request, slug):
    # создаем корзину (получаем из сессии)
    cart = Cart(request)

    product = get_object_or_404(Product, slug=slug)
    cart.add(product=product)

    return redirect('shop:index')


def cart_detail(request):
    cart = Cart(request)
    return render(request, template_name='cart/cart_detail.html', context={'cart': cart})


@csrf_exempt
def update_cart_by_front(request):
    data = json.loads(request.body)
    print(data)
    print(type(data))
    product_id = data.get('productIdValue')
    quantity = data.get('quantityValue')

    if product_id:
        cart = Cart(request)

        product = get_object_or_404(Product, pk=int(product_id))
        cart.add(product=product, quantity=int(quantity), override_quantity=True)
        print('ok', cart.cart)
        response_data = {'result': 'success'}
    else:
        response_data = {'result': 'failed'}

    return JsonResponse(response_data)


