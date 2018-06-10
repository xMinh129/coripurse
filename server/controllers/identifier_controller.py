from flask import request, json, jsonify, Response
import requests

from server.helpers.face_verification_helper import update_data

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


class IdentifierController(object):

    def __init__(self, app):
        @app.route('/api/verifyAccount', methods=['POST'])
        def verify_account_with_face_image():
            try:
                is_verified, name = update_data(3)
                if is_verified:
                    return jsonify({'success': is_verified, 'name': name})
                else:
                    return jsonify({'success': is_verified})
            except Exception:
                return jsonify({'success': False})