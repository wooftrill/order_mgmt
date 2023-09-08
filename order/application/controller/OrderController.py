
import logging,json
from http import HTTPStatus
from dataclasses import asdict
from flask import jsonify, make_response,request
from order.application.model.Error import Error
from order.application.model.OrderGwModel import OrderGwModel

from order.application.service.SQLOrmService import SQLOrmService
from order.application.service.SQLOrmService import sql_orm_service
from order.application.service.FirebaseJWTClient import firebase_jwt_client
from order.application import app

logging.getLogger().setLevel(logging.INFO)


class OrderController:
    def __init__(self,s: SQLOrmService):
        self.service = s


order_controller = OrderController(sql_orm_service)


@app.get('/')
def welcome():
    return "Welcome to service"


def cors_preflight():
    # Respond to the OPTIONS preflight request with the necessary CORS headers
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST')

    return response


# Handle the OPTIONS request for /sign_in/ separately
app.add_url_rule('/forward_to_Order', view_func=cors_preflight, methods=['OPTIONS'])


@app.post('/forward_to_Order',endpoint='forward_to_Order')
@firebase_jwt_client.jwt_required
def forward_to_order(response):
    """

    :param response:
    :return:
    """
    logging.info("POST /forward_to_Order")
    if not response:
        logging.error("Could not generate session_id")
        return HTTPStatus.BAD_REQUEST, 401
    try:
        gw_model = asdict(OrderGwModel(response["user_id"],response["session_id"]))
        print(gw_model)
        response= sql_orm_service.generate_order(gw_model)
        logging.info("new",response)
        if response is False :
            error= Error(message="No Items in cart",message_id=HTTPStatus.BAD_REQUEST, type=404)
            return make_response(jsonify(error, HTTPStatus.BAD_REQUEST))
        elif response is None:
            error = Error(message="Internal Server Error", message_id=HTTPStatus.INTERNAL_SERVER_ERROR, type=500)
            return make_response(jsonify(error, HTTPStatus.BAD_REQUEST))
        else:
            return jsonify(response,HTTPStatus.OK)
    except Exception as ex:
        logging.error(f"issue with processing {ex}")






