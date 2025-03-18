from flask import jsonify
from Model.User import User
import jwt
import datetime

SECRET_KEY = "I am a secret key"

def register_user(request):
    data = request

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    user = User(fullName=data.get("fullName"), username=data.get("username"), password=data.get("password"), profile_url=data.get("profile_url", ""), token="")
    
    response = user.create()
    return jsonify(response), response.get("statusCode")


