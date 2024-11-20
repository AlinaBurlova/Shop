import uuid
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from .models import Order, OrderItem
from .forms import OrderForm
from cart.views import Cart, ProductCartUser
from cart.models import CartItem
from shop.models import Product


@csrf_exempt
def new_quick_order(request):
    data = json.loads(request.body)
    name = data.get('name')
    last_name = data.get('lastName')
    email = data.get('email')
    phone = data.get('phone')
    delivery = data.get('delivery')
    payment = data.get('payment')

    cart = Cart(request)

    order = Order.objects.create(name=name,
                                 last_name=last_name,
                                 email=email,
                                 phone=phone,
                                 delivery=delivery,
                                 payment=payment,
                                 number=uuid.uuid4(),
                                 )

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'])

    # orders = OrderItem.objects.filter(order=order)
    # cart_order = cart.copy()
    cart.clear()

    url = reverse("main")
    json_response = {"status": "ok", "url": url}
    return JsonResponse(json_response)
    # return render(request, template_name='orders/order_create.html', context={'cart_order': cart_order})


def new_order(request):
    cart = ProductCartUser(request)

    if request.method == "GET":
        order_form = OrderForm()
        context = {"form": order_form}
        return render(request, template_name='orders/order_add.html', context=context)

    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.number = uuid.uuid4()
            order.user = request.user
            order.cart = cart.user_cart
            order.name = request.user.username
            order.last_name = request.user.last_name
            order.email = request.user.email
            order.phone = request.user.phone

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order_form.instance, product=item['product'], quantity=item['quantity'])

            cart.user_cart.delete()

        context = {"order": order_form.instance}
        return render(request, template_name='orders/order_create.html', context=context)


# @login_required
# def orders_list(request):
#     orders = Order.objects.filter(user=request.user)
#     context = {"orders": orders}
#
#     return render(request, template_name='orders/orders.html', context=context)
#
#
# def order_detail(request, number):
#     order = get_object_or_404(Order, number=number, user=request.user)
#     context = {"order": order}
#
#     return render(request, template_name='orders/order_detail.html', context=context)


@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/orders.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    slug_field = 'number'
    slug_url_kwarg = 'number'
