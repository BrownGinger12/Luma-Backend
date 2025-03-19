from flask import jsonify
from Model.User import User
import jwt
import datetime
from pydantic import ValidationError

SECRET_KEY = "I am a secret key"

def register_user(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user = User(fullName=data.get("fullName"), username=data.get("username"), password=data.get("password"), profile_url=data.get("profile_url", ""), token="")
        
        response = user.create()
        return jsonify(response), response.get("statusCode")
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

def login_user(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400


        user = User.get("username", data.get("username"))
        if user.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        user = user.get("data")

        if User.verify_password(data.get("password"), user.get("password")):
            user["token"] = jwt.encode({"user_id": user.get("user_id"), "username": user.get("username"), "profile_url": user.get("profile_url"), "fullName": user.get("fullName"), "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)

        if not user.get("token"):
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({"token": user.get("token")}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def edit_user(request, user_id):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user = User.get("user_id", user_id)

        if user.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        
        response = User.update(user_id, data)    
        
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_user(user_id):
    try:
        user = User.get("user_id", user_id)

        if user.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404

        response = User.delete(user_id)
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    