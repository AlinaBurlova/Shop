import uuid
import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

from .models import Order, OrderItem
from .forms import OrderForm
from cart.views import Cart, ProductCartUser
from cart.models import CartItem
from shop.models import Product


user = get_user_model()



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


@login_required
def orders_list(request):
    admin = user.objects.get(username='staff')
    if request.user == admin:
        orders = Order.objects.all()
        context = {"orders": orders, "current_page": 'orders',}
        return render(request, template_name='orders/orders.html', context=context)

    orders = Order.objects.filter(user=request.user)
    context = {
        "orders": orders,
    }

    return render(request, template_name='orders/orders.html', context=context)

@login_required
def order_detail(request, number):
    admin = user.objects.get(username='staff')
    if request.user == admin:
        order = get_object_or_404(Order, number=number)
        order_items = order.order_items.all()
        context = {"order": order, "order_items": order_items}
        return render(request, template_name='orders/order_detail.html', context=context)

    order = get_object_or_404(Order, number=number, user=request.user)
    order_items = order.order_items.all()
    context = {"order": order, "order_items": order_items}

    return render(request, template_name='orders/order_detail.html', context=context)


# class OrderListView(ListView):
#     model = Order
#     template_name = 'shop/admin/orders.html'
#     context_object_name = 'orders'
#
#
# class OrderDetailView(DetailView):
#     model = Order
#     template_name = 'orders/order_detail.html'
#     context_object_name = 'order'
#     slug_field = 'number'
#     slug_url_kwarg = 'number'

def all_order_list(request):
    admin = user.objects.get(username='staff')
    if request.user != admin:
        raise PermissionError

    print(type(admin))

    orders = Order.objects.all()
    context = {"orders": orders}

    return render(request, template_name='shop/admin/orders.html', context=context)
