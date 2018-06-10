from flask import Response, json
import requests

JSON_RESPONSE_TYPE = 'application/json'

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': ['OPTIONS', 'GET', 'POST'],
    'Access-Control-Allow-Headers': 'Content-Type'
}


def handle_response(response):
   if response:
        return Response(json.dumps(response), status=requests.codes.ok, mimetype=JSON_RESPONSE_TYPE, headers=HEADERS)
   else:
        return Response(json.dumps({'error': response.get('error')}), status=requests.codes.server_error,
                        mimetype=JSON_RESPONSE_TYPE, headers=HEADERS)
