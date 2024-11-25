import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Keyboard
from django.views.decorators.csrf import csrf_exempt
from .functions import token_request, prepare_order


def cart(request):
    keyboard = Keyboard()
    inicial_cart = {
    'products': keyboard,
    'totalsum': keyboard.price,
    'json':keyboard.__dict__()
}
    return render(request, 'cart.html', inicial_cart)


@csrf_exempt
def createorder(request):
    json_data = json.loads(request.body)
    access_token = token_request()
    headers, data = prepare_order(access_token, json_data)
    call = requests.post('https://api.sandbox.paypal.com/v2/checkout/orders', headers=headers, data=data)
    return JsonResponse(call.json())


@csrf_exempt
def checkout(request):
    dados = json.loads(request.body)
    orderID = dados['orderID']

    access_token = token_request()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    call = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture', headers=headers)
    dados['url'] = f'https://kaiosatiro.pythonanywhere.com/confirmation?orderid={orderID}'

    return JsonResponse(dados)


def confirmation(request):
    return render(request, 'confirmation.html')



