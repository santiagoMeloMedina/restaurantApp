import json
from flask import Flask, jsonify, request
from service.registration import handler as registration_handler
from service.login import handler as login_handler
from service.crud import create as create_restaurant, update as update_restaurant, get_private as get_private_restaurants, get_public as get_public_restaurants

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

@app.route("/restaurant/private", methods=["GET"])
def get_private():
    event = {"body": {}, "headers": request.headers}
    return jsonify(get_private_restaurants.handler(event, {}))

@app.route("/restaurant/<int:limit>/<int:offset>", methods=["GET"])
def get_public(limit, offset):
    event = {"body": {}, "headers": request.headers, "params": {"limit": limit, "offset": offset}}
    return jsonify(get_public_restaurants.handler(event, {}))

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)