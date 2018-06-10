from flask import request, json, jsonify, Response
import requests
from server.models.connect_db import db
from bson.json_util import dumps

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


class UserController(object):

    def __init__(self, app):

        @app.route('/api/registerCustomer', methods=['POST'])
        def register_customer():
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
            payload = json.loads(request.data)
            payload['ApplicationToken'] = "51b4fbed-28d5-4735-8b7d-97394a32ddb5"
            r = requests.post(' https://webservices.coriunder.cloud/v2/customer.svc/RegisterCustomer', headers=headers,
                              data=json.dumps(payload))
            return jsonify({'user': r.json()})

        # TODO to put the application token into config file
        @app.route('/api/login', methods=['POST'])
        def login():
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
            payload = {
                "email": request.values['email'],
                "password": request.values['password'],
                "options": {
                    "applicationToken": "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                    "userRole": "15"
                }
            }
            r = requests.post('https://webservices.coriunder.cloud/v2/account.svc/LogIn', headers=headers,
                              data=json.dumps(payload))
            cloud_token = r.json()["d"]["CredentialsToken"]
            company_hash = "3Yv6kN8L"
            signature = "bytes-SHA256, " + base64.b64encode(hashlib.sha256(company_hash.encode('utf-8')).digest()).decode('utf-8')
            user_headers = {'Content-type': JSON_RESPONSE_TYPE,
                            'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                            "Signature": signature, "coriunder_cloud_Token": cloud_token}
            user = requests.post('https://webservices.coriunder.cloud/v2/customer.svc/GetCustomer',
                                 headers=user_headers)
            if user:
                response = jsonify(user=user.json(), token=cloud_token)
                return response
            else:
                return handle_response({'error': "Cannot find user"})

        @app.route('/api/getCustomer', methods=['POST'])
        def get_customer_info():
            company_hash = request.headers['Company-Hash'].encode('utf-8')
            signature = "bytes-SHA256, " + base64.b64encode(hashlib.sha256(company_hash.encode('utf-8')).digest()).decode('utf-8')
            coriunder_cloud_Token = request.headers['Coriunder-Cloud-Token']
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                       "coriunder_cloud_Token": coriunder_cloud_Token, "Signature": signature}

            r = requests.post('https://webservices.coriunder.cloud/v2/customer.svc/GetCustomer', headers=headers)
            return handle_response(r.json())

        @app.route('/api/updatePinCode', methods=['POST'])
        def update_pin_code():
            company_hash = request.headers['Company-Hash']
            request_body = request.data
            string_to_hash =  request_body + company_hash
            signature = "bytes-SHA256, " + base64.b64encode(hashlib.sha256(string_to_hash.encode('utf-8')).digest()).decode('utf-8')
            coriunder_cloud_Token = request.headers['Coriunder-Cloud-Token']
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                       "coriunder_cloud_Token": coriunder_cloud_Token, "Signature": signature}

            r = requests.post('https://webservices.coriunder.cloud/v2/account.svc/UpdatePincode',
                              data=request.data,
                              headers=headers)

            return handle_response(r.json())

        @app.route('/api/signInWithImage', methods=['POST'])
        def sign_in_with_image():
            name = request.values['name']
            user = json.loads(dumps(db.users.find({'name': name})))[0]
            print(user)
            if user:
                headers = {'Content-type': JSON_RESPONSE_TYPE,
                           'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5"}
                payload = {
                    "email": user['email'],
                    "password": user['password'],
                    "options": {
                        "applicationToken": "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                        "userRole": "15"
                    }
                }
                r = requests.post('https://webservices.coriunder.cloud/v2/account.svc/LogIn', headers=headers,
                                  data=json.dumps(payload))
                cloud_token = r.json()["d"]["CredentialsToken"]
                company_hash = "3Yv6kN8L"
                signature = "bytes-SHA256, " + base64.b64encode(
                    hashlib.sha256(company_hash.encode('utf-8')).digest()).decode('utf-8')
                user_headers = {'Content-type': JSON_RESPONSE_TYPE,
                                'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                                "Signature": signature, "coriunder_cloud_Token": cloud_token}
                user = requests.post('https://webservices.coriunder.cloud/v2/customer.svc/GetCustomer',
                                     headers=user_headers)
                if user:
                    response = jsonify(user=user.json(), token=cloud_token)
                    return response
                else:
                    return handle_response({'error': "Cannot find user"})

            else:
                return jsonify({'error': "no user found"})



