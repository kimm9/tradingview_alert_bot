
import json, config, ccxt
from flask import Flask, request
from flask.wrappers import Request
from ftx import FtxClient


app = Flask(__name__)
ftx = ccxt.ftx({
    'apiKey': config.API_KEY,
    'secret': config.SECRET_KEY,
})


def order(symbol, order_type, side, quantity):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = ftx.create_order(symbol, order_type, side, quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/webhook', methods=['POST'])
def webhook():
    # print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return{
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    print(data['ticker'])
    print(data['strategy']['order_action'])
    side = data['strategy']['order_action']
    quantity = data['strategy']['order_contracts']
    symbol = data['ticker']


    order_response = order(symbol, "market", side, quantity)

    if order_response:
        return {
            "code": "success",
            "message": data
        }
    else:
        print('order failed')

        return {
            "code": "error",
            "message": "order failed"
        }