from flask import Flask, jsonify, make_response, request
from Handler.User_Handler import register_user, login_user, edit_user, delete_user
from Handler.Employee_Handler import register_employee, login_employee, edit_employee, delete_employee
from Handler.room_handler import add_room, get_room, get_all_rooms, search_rooms, update_room, delete_room
from Handler.review_handler import *
from Handler.transaction_handler import add_transaction, get_all_transactions, get_transaction, update_transaction, delete_transaction
from Handler.luma_events_handler import add_event, get_all_events, get_event, update_event, delete_event
from Handler.package_handler import add_package, get_all_packages, get_package, update_package, delete_package
from functools import wraps
from Model.User import User
from Model.employee import Employee
import jwt

app = Flask(__name__)

SECRET_KEY = "I am a secret key"

def user_token_required(f):
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

            if "password" in current_user["data"]:
                del current_user["data"]["password"]

            if current_user.get("statusCode") != 200:
                return jsonify({"error": f"User not found! {current_user}"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return f(current_user["data"], *args, **kwargs)
        
    return decorated

def employee_token_required(f):
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
            current_employee = Employee.get('user_id', data['user_id'])
            if "password" in current_employee["data"]:
                del current_employee["data"]["password"]

            if current_employee.get("statusCode") != 200:
                return jsonify({"error": f"User not found! {current_employee}"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        return f(current_employee["data"], *args, **kwargs)
        
    return decorated



@app.route("/")
@user_token_required
def hello_from_root(current_user):
    return jsonify(message='Hello from root!')

@app.route("/hello")
@user_token_required
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
@user_token_required
def update_user(current_user):
    data = request.get_json()

    return edit_user(data, current_user.get("user_id"))

@app.route("/delete_user", methods=['DELETE'])
@user_token_required
def del_user(current_user):
    return delete_user(current_user.get("user_id"))

@app.route("/get_user", methods=['GET'])
@user_token_required
def get_user(current_user):
    return jsonify(current_user), 200

@app.route("/rooms", methods=['GET'])
def get_rooms():
    return get_all_rooms(request)

@app.route("/room/search/<room_name>", methods=['GET'])
def search_multiple_rooms(room_name):
    return search_rooms(request, attribute="room_name", atr_value=room_name)

@app.route("/room/<room_id>", methods=['GET'])
def get_one_room(room_id):
    return get_room(request, room_id=room_id)	

@app.route("/room", methods=['POST'])
def create_room():
    response = add_room(request)
    return response

@app.route("/room/<room_id>", methods=['PUT'])
@employee_token_required
def update_one_room(room_id):
    response = update_room(request, room_id=room_id)
    return response

@app.route("/room/<room_id>", methods=['DELETE'])
@employee_token_required
def delete_one_room(room_id):
    response = delete_room(request, room_id=room_id)
    return response

@app.route("/transaction", methods=['POST'])
def add_one_transaction():
    return add_transaction(request)

@app.route("/transactions", methods=['GET'])
def get_transactions():
    return get_all_transactions(request)

@app.route("/transaction/<reservation_id>", methods=['GET'])
def get_one_transaction(reservation_id):
    return get_transaction(request, reservation_id)

@app.route("/transaction/<reservation_id>", methods=['PUT'])
@employee_token_required
def update_one_transaction(reservation_id):
    return update_transaction(request, reservation_id)

@app.route("/transaction/<reservation_id>", methods=['DELETE'])
@employee_token_required
def delete_one_transaction(reservation_id):
    return delete_transaction(request, reservation_id)

@app.route("/event", methods=['POST'])
def add_one_event():
    return add_event(request)

@app.route("/events", methods=['GET'])
def get_events():
    return get_all_events(request)

@app.route("/event/<event_id>", methods=['GET'])
def get_one_event(event_id):
    return get_event(request, event_id)

@app.route("/event/<event_id>", methods=['PUT'])
@employee_token_required
def update_one_event(event_id):
    return update_event(request, event_id)

@app.route("/event/<event_id>", methods=['DELETE'])
@employee_token_required
def delete_one_event(event_id):
    return delete_event(request, event_id)

@app.route("/package", methods=['POST'])
def add_one_package():
    return add_package(request)

@app.route("/packages", methods=['GET'])
def get_packages():
    return get_all_packages(request)

@app.route("/package/<package_id>", methods=['GET'])
def get_one_package(package_id):
    return get_package(request, package_id)

@app.route("/package/<package_id>", methods=['PUT'])
@employee_token_required
def update_one_package(package_id):
    return update_package(request, package_id)

@app.route("/package/<package_id>", methods=['DELETE'])
@employee_token_required
def delete_one_package(package_id):
    return delete_package(request, package_id)

@app.route("/create_employee", methods=['POST'])
def create_employee():
    data = request.get_json()

    return register_employee(data)

@app.route("/login_employee", methods=['POST'])
def signin_employee():
    data = request.get_json()

    return login_employee(data)

@app.route("/update_employee", methods=['PUT'])
@employee_token_required
def update_employee(current_employee):
    data = request.get_json()

    return edit_employee(data, current_employee.get("user_id"))

@app.route("/delete_employee", methods=['DELETE'])
@employee_token_required
def del_employee(current_employee):
    return delete_employee(current_employee.get("user_id"))

@app.route("/get_employee", methods=['GET'])
@employee_token_required
def get_employee(current_employee):
    return jsonify(current_employee), 200

#review routes
@app.route("/create_review", methods=['POST'])
@user_token_required
def create_review(current_user):
    return add_review(request, current_user.get("user_id"))

@app.route("/review/<reservation_id>", methods=['GET'])
def get_rev(reservation_id):
    return get_review(reservation_id)


@app.route("/review/<reservation_id>", methods=['DELETE', 'PUT'])
@user_token_required
def rev_ud(current_user, reservation_id):
    method_handler = {
        'DELETE': delete_review,
        'PUT': update_review
    }
    
    if request.method == 'PUT':
        return method_handler[request.method](request, reservation_id)
    
    return method_handler[request.method](reservation_id)

@app.route("/reviews/room/<room_id>", methods=['GET'])
def get_reviews(room_id):
    return get_reviews_room(room_id)



@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)

if __name__ == "__main__":
    app.run(debug=True)