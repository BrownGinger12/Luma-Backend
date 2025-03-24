from flask import jsonify
from Model.employee import Employee
import jwt
import datetime
from pydantic import ValidationError

SECRET_KEY = "I am a secret key"    

def register_employee(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        employee = Employee(fullName=data.get("fullName"), username=data.get("username"), password=data.get("password"), profile_url=data.get("profile_url", ""), employee_role=data.get("employee_role"), email=data.get("email", ""))
        
        response = employee.create()
        return jsonify(response), response.get("statusCode")
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


def login_employee(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400


        employee = Employee.get("username", data.get("username"))
        if employee.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        employee = employee.get("data")
        if Employee.verify_password(data.get("password"), employee.get("password")):
            employee["token"] = jwt.encode({"user_id": employee.get("user_id"), 
                                            "employee_role": employee.get("employee_role"), 
                                            "username": employee.get("username"), 
                                            "profile_url": employee.get("profile_url"), 
                                            "fullName": employee.get("fullName"),
                                            "enail": employee.get("email"),
                                            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 
                                            SECRET_KEY)

        if not employee.get("token"):
            return jsonify({"error": f"Invalid credentials {employee}"}), 401

        return jsonify({"token": employee.get("token")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def edit_employee(request, user_id):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400

        employee = Employee.get("user_id", user_id)

        if employee.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        
        response = Employee.update(user_id, data)    
        
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_employee(user_id):
    try:
        employee = Employee.get("user_id", user_id)

        if employee.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        response = Employee.delete(user_id)
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def update_user_image(event, context):
    try:
        print(event)
         
        if 'detail' in event:
            body = event['detail']
            user_id = body['user_id']
            file_url = body['image_url']
            
            response = Employee.update(user_id, {"profile_url": file_url})

            if response.get("statusCode") == 404:
                return {"message": "user not found"}, 404
            if response.get("statusCode") == 500:
                return {"message": "Internal server error"}, 500
            
            return response
        
    except ValueError as e:
        # event = EventbridgeEvent(
        #     "transaction_on_failure",
        #     {"message": str(e), "reservation_id": body["reservation_id"]}
        # )
        # event.send()
        return {"message": e}
    