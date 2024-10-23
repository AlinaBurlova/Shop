from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect

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

    # сохранений изменений в сессии
    def save(self):
        self.session.modified = True


    # метод помещения товара в корзину
    def add(self, product, quantity=1, override_quantity=False):
        # получаем id товара из объекта товара
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
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


    # метод подсчета общего количества элемента
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        # return len(self.cart) - количество типов товара (без учета количества каждого товара)


    # метод общего подсчета
    def get_total_price(self):
        return sum(Decimal(item["price"]) *  item["quantity"] for item in self.cart.values())


    def clear(self):
        self.cart.clear()  # очистить
        # del self.session[CART_SESSION_ID]  # удалить полностью
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

def cart_add(request, product_id):
    # создаем корзину
    cart = Cart(request)

    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)

    return redirect('shop:index')


def cart_detail(request):
    cart = Cart(request)
    return render(request, template_name='cart/cart_detail.html', context={'cart': cart})



