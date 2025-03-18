from flask import Flask, jsonify, make_response, request
from Handler.User_Handler import register_user


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

    return register_user(data)

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)