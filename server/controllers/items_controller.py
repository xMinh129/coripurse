from flask import request, json, jsonify, Response
import requests

# Using sha256 hashing algorithm and base64 encoder
import hashlib
import base64

from server.handlers.response_handler import handle_response

JSON_RESPONSE_TYPE = 'application/json'

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': ['OPTIONS', 'GET', 'POST'],
    'Access-Control-Allow-Headers': 'Content-Type'
}


class ItemsController(object):
    def __init__(self, app):
        @app.route('/api/getItems', methods=['POST'])
        def get_items():
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
            payload = {
                "filters": {
                    "Language": "EN",
                    "MerchantNumber": "3771097",
                    "ShopId": 1
                },
                "sortAndPage": {
                    "PageNumber": 2,
                    "PageSize": 5
                }
            }
            r = requests.post('https://webservices.coriunder.cloud/v2/shop.svc/GetProducts', headers=headers,
                              data=json.dumps(payload))

            # Return an array of items
            return jsonify({"items": r.json()})

        @app.route('/api/addToCart', methods=['POST'])
        def add_to_cart():
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
            if 'cartCookie' in request.values:
                cart_cookie = request.values['cartCookie'].replace(" ", "+")

            else:
                cart_cookie = False
            cart_payload = {
                "cookie": cart_cookie
            }
            cart_request = requests.post('https://webservices.coriunder.cloud/v2/shop.svc/GetCart', headers=headers,
                                         data=json.dumps(cart_payload))
            new_items = {
                "ProductId": request.values['productId'],
                "Price": request.values['price'],
                "Quantity": request.values['quantity']
            }
            if cart_request.json().get('d'):
                remapped_existing_items = []
                existing_items = cart_request.json().get('d').get('Items')
                for i in existing_items:
                    item = {
                        "ProductId": i.get('ProductId'),
                        "Price": i.get('Price'),
                        "Quantity": i.get('Quantity')
                    }
                    remapped_existing_items.append(item)

                all_items = remapped_existing_items + [new_items]
                number_of_items = len(all_items)
                total_price = 0
                for i in all_items:
                    if type(i.get('Price')) == float:
                        price = i.get('Price')
                    else:
                        price = float(str(i.get('Price')))
                    total_price = total_price + price
                add_cart_payload = {
                    "cart": {
                        "Items": all_items,
                        "CurrencyIso": "USD",
                        "MerchantNumber": 3771097,
                        "Cookie": cart_cookie
                    }
                }

                add_cart_request = requests.post('https://webservices.coriunder.cloud/v2/shop.svc/SetCart',
                                                 headers=headers,
                                                 data=json.dumps(add_cart_payload))
            else:
                add_cart_payload = {
                    "cart": {
                        "Items": [new_items],
                        "CurrencyIso": "USD",
                        "MerchantNumber": 3771097
                    }
                }
                number_of_items = len([new_items])
                total_price = new_items.get('Price')
                add_cart_request = requests.post('https://webservices.coriunder.cloud/v2/shop.svc/SetCart',
                                                 headers=headers,
                                                 data=json.dumps(add_cart_payload))

            # Return a cart cookie
            return jsonify({"cookie": add_cart_request.json(), "size": number_of_items, 'total': total_price})

        @app.route('/api/getCart', methods=['POST'])
        def get_cart():
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
            cart_cookie = request.values['cartCookie']
            cart_payload = {
                "cookie": cart_cookie
            }
            cart_request = requests.post('https://webservices.coriunder.cloud/v2/shop.svc/GetCart', headers=headers,
                                         data=json.dumps(cart_payload))
            return jsonify({'cart': cart_request.json()})
