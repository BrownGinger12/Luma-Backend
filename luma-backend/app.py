from flask import Flask, jsonify, make_response, request
from Handler.User_Handler import register_user, login_user, edit_user, delete_user
from functools import wraps
from Model.User import User
import jwt

app = Flask(__name__)

SECRET_KEY = "I am a secret key"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if the token is in the request headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"error": "Token is missing!"}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.get('user_id', data['user_id'])
            if current_user.get("statusCode") != 200:
                return jsonify({"error": "User not found!"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return f(current_user["data"], *args, **kwargs)
        
    return decorated


@app.route("/")
@token_required
def hello_from_root(current_user):
    return jsonify(message='Hello from root!')

@app.route("/hello")
@token_required
def hello(current_user):
    return jsonify(message='Hello from path!'), 200

@app.route("/create_user", methods=['POST'])
def create_user():
    data = request.get_json()

    return register_user(data)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()

    return login_user(data)

@app.route("/update_user", methods=['PUT'])
@token_required
def update_user(current_user):
    data = request.get_json()

    return edit_user(data, current_user.get("user_id"))

@app.route("/delete_user", methods=['DELETE'])
@token_required
def del_user(current_user):
    return delete_user(current_user.get("user_id"))

@app.route("/get_user", methods=['GET'])
@token_required
def get_user(current_user):
    return jsonify(current_user), 200

@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)