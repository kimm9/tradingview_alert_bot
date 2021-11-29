from flask import Flask
from flask.wrappers import Request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/webhook', methods=['POST'])
def webhook():
    print(request)

    return {
        "code": "success"
    }