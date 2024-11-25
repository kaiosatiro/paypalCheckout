import requests
import json
from pathlib import os
from .models import Keyboard
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = str(os.getenv('CLIENTID'))
CLIENT_KEY = str(os.getenv('CLIENTKEY'))

def token_request():    
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'pt_BR',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        headers=headers,
        data=data,
        auth=('AV7gkp9bqCT6IYdxhnSh4o9w4ZDHxsghpFDaC_kRkJXPJRnajExhpBFrtJwKBL6ng3roaMXMdtPOY5UB', 'EBKWSh3AYaJ6kbbXf9Uz8c-u5n8jNF65xCTZ2LZdOBJ5HgjmeBzsufvRB8FD4TIKfVjWpWJ8XGek4nGe'),
    )
    return dict(response.json())['access_token']


def prepare_order(access_token, json_data):
    product_list = json_data['cart']

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}',
    }
    dic = {
    "intent":"CAPTURE",
    "purchase_units":[
        {
            "reference_id":product_list[0]['sku'],
            "amount":{
                "currency_code":"USD",
                "value": Keyboard.price * int(product_list[0]['quantity'])
            },
            "payee":{
                "email_address": "sb-ixvfa26639146@business.example.com"
            },
            # "shipping":{
                # "type": "SHIPPING",
                # "name": {
                    # "given_name": "Persona",
                    # "surname": "Doe"
                # },
                # "address":{
                    # "address_line_1": "1 Main St",
                    # "address_line_2": "Apt",
                    # "admin_area_2": "San Jose",
                    # "admin_area_1": "CA",
                    # "postal_code": "95131",
                    # "country_code": "US"
                # }
            # }
            
        }
    ],
    "payment_source":{
        "paypal":{
            "experience_context":{
                "payment_method_preference":"IMMEDIATE_PAYMENT_REQUIRED",
                "brand_name":"SATIRO",
                "locale":"pt-BR",
                "landing_page":"LOGIN",
                "shipping_preference":"GET_FROM_FILE", #SET_PROVIDED_ADDRESS GET_FROM_FILE NO_SHIPPING
                "user_action":"PAY_NOW",
            },
            "email_address": json_data['email'],
            "name":{
                "given_name": json_data['firstname'],
                "surname": json_data['lastname']
            },
            "phone":{
                "phone_number":{
                    "national_number": json_data['phonenumber']
                }
            },
            "address":{
                "address_line_1": json_data['addressone'],
                "address_line_2": "Apt",
                "admin_area_2": json_data['addresstwo'],
                "admin_area_1": json_data['state'],
                "postal_code": json_data['zipcode'],
                "country_code": json_data['country']
            }
        }
    }
    }   
    data =  json.dumps(dic, separators=(',', ':'))
    
    return headers, data
