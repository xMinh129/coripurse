from flask import request, json, jsonify, Response
import requests

from collections import OrderedDict

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


class BalanceController(object):

    def __init__(self, app):
        @app.route('/api/getBalance', methods=['POST'])
        def get_total_balance():
            company_hash = request.headers['Company-Hash']
            string_to_hash = json.dumps({
                'currencyIsoCode': str(request.values['currencyIsoCode'])
            }) + str(company_hash)
            signature = "bytes-SHA256, " + base64.b64encode(
                hashlib.sha256(string_to_hash.encode('utf-8')).digest()).decode('utf-8')
            coriunder_cloud_Token = request.headers['Coriunder-Cloud-Token']
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                       "coriunder_cloud_Token": coriunder_cloud_Token, "Signature": signature}

            r = requests.post('https://webservices.coriunder.cloud/v2/balance.svc/GetTotal',
                              data=json.dumps({
                                  'currencyIsoCode': str(request.values['currencyIsoCode'])
                              }),
                              headers=headers)

            return handle_response(r.json())

        @app.route('/api/transferBalance', methods=['POST'])
        def transfer_balance():
            company_hash = "3Yv6kN8L"
            request_body = json.dumps(
                OrderedDict(destAcocuntId=request.values['destAccountId'], amount=float(request.values['amount']),
                            currencyIso=request.values['currencyIso'], pinCode=request.values['pinCode']),
                sort_keys=False)
            string_to_hash = request_body + company_hash
            signature = "bytes-SHA256, " + base64.b64encode(
                hashlib.sha256(string_to_hash.encode('utf-8')).digest()).decode('utf-8')
            coriunder_cloud_Token = request.headers['Coriunder-Cloud-Token']
            headers = {'Content-type': JSON_RESPONSE_TYPE, 'applicationToken': "51b4fbed-28d5-4735-8b7d-97394a32ddb5",
                       "coriunder_cloud_Token": coriunder_cloud_Token, "Signature": signature}

            r = requests.post('https://webservices.coriunder.cloud/v2/balance.svc/TransferAmount',
                              data=request_body,
                              headers=headers)

            return handle_response(r.json())
