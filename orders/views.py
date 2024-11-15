import json
from cgitb import reset
from http.client import responses

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from cart.views import Cart

@csrf_exempt
def new_quick_order(request):
    data = json.loads(request.body)

    response = {"status": "ok"}

    return JsonResponse(response)

def new_order():
    pass