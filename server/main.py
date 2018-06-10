from flask import Flask, Response, json
from flask_cors import CORS

from server.controllers.users_controller import UserController
from server.controllers.balance_controller import BalanceController
from server.controllers.items_controller import ItemsController
from server.controllers.identifier_controller import IdentifierController

app = Flask(__name__, static_folder="./static/dist", template_folder="./static")
cors = CORS(app)

UserController(app)
BalanceController(app)
ItemsController(app)
IdentifierController(app)


@app.route('/health_check', methods=['GET'])
def health_check():
    """
    Health check
    """
    return Response(json.dumps({'reply': 'I\'m ok'}))
