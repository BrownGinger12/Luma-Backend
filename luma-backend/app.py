from flask import Flask, jsonify, make_response, request
from Model.User import User
from Gateways.DynamoDB_Gateway import DynamoDB


app = Flask(__name__)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/hello")
def hello():
    return jsonify(message='Hello from path!')

@app.route("/create_user", methods=['POST'])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user = User(fullName=data.get("fullName"), username=data.get("username"), password=data.get("password"), profile_url=data.get("profile_url", ""), token="")
    
    response = user.create()
    return jsonify(response), response.get("statusCode")

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)