import json
from flask import Flask, jsonify, request
from service.registration import handler as registration_handler

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"hi"})

@app.route("/register", methods=["POST"])
def register():
    event = {"body": request.get_json(), "headers": {}}
    return jsonify(registration_handler.handler(event, {}))


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)