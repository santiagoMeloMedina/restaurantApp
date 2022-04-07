import json
from flask import Flask, jsonify, request
from service.registration import handler as registration_handler
from service.login import handler as login_handler
from service.crud import create as create_restaurant, update as update_restaurant

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"hi"})

@app.route("/register", methods=["POST"])
def register():
    event = {"body": request.get_json(), "headers": request.headers}
    return jsonify(registration_handler.handler(event, {}))

@app.route("/login", methods=["POST"])
def login():
    event = {"body": request.get_json(), "headers": request.headers}
    return jsonify(login_handler.handler(event, {}))

@app.route("/restaurant", methods=["POST"])
def create():
    event = {"body": request.get_json(), "headers": request.headers}
    return jsonify(create_restaurant.handler(event, {}))

@app.route("/restaurant", methods=["PUT"])
def update():
    event = {"body": request.get_json(), "headers": request.headers}
    return jsonify(update_restaurant.handler(event, {}))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)