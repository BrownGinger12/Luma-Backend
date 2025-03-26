from flask import jsonify
from Model.User import User
import jwt
import datetime
from pydantic import ValidationError
import requests
from Gateways.Cognito_Gateway import Cognito

SECRET_KEY = "I am a secret key"


def register_user(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        user = User(user_id=data.get("user_id"), fullName=data.get("fullName"), username=data.get("username"), password=data.get("password"), profile_url=data.get("profile_url", ""), email=data.get("email", ""))
        
        response = user.create()
        return jsonify(response), response.get("statusCode")
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

def login_user(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400

        resp = Cognito().login_user(username=data["username"], password=data["password"])

        if resp["statusCode"] != 200:
            return jsonify({"message": resp["message"]}), resp["statusCode"]
        
        return jsonify({"token": resp["AccessToken"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def edit_user(request, user_id, access_token):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user = User.get("user_id", user_id)

        if user.get("statusCode") == 404:
            return jsonify({"error": "User not found"}), 404
        
        user = user.get("data")
        
        if data.get("old_password") and data.get("new_password"):
            resp = Cognito().change_password(access_token, data.get("old_password"), data.get("new_password"))
            
            if resp.get("statusCode") != 200:
                return jsonify({"message": resp.get("message")}), resp.get("statusCode")
        
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
    
def update_user_image(event, context):
    try:
        print(event)
         
        if 'detail' in event:
            body = event['detail']
            user_id = body['user_id']
            file_url = body['image_url']
            
            response = User.update(user_id, {"profile_url": file_url})

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
    
def get_all_users():
    try:
        response = User.get_all()

        if response.get("statusCode") == 404:
            return jsonify({"error": "No users found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"error": "Internal server error"}), 500
        
        if response.get("data") == []:
            return jsonify({"error": "No users found"}), 404
        
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def verify_user(request):
    try:
        data = request

        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        resp = Cognito().confirm_user(data["username"], data["confirmation_code"])
        
        return jsonify({"message": resp.get("message")}), resp.get("statusCode")
 
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

# untested yet on PYTHON, but working on POSTMAN
# basically we want to send a GET request on the github API below
# to confirm if the user is logged in using the token provided by github

# these two functions are for token exchange from Github to Backend
# 1. github token -> backend
# 2. backend jwt token -> frontend
# sign-in with github, generates its own github token
def token_exchange(request):
    try:
        data = request

        token = data.get("AUTH_TOKEN")
        github_user = verify_github_token(token)
        if not github_user:
            return jsonify({"error": "Invalid GitHub token"}), 401

        jwt_token = jwt.encode({
            "user_id": github_user.get("id"),
            "username": github_user.get("login"),
            "profile_url": github_user.get("avatar_url"),
            "fullName": github_user.get("name"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, SECRET_KEY)

        return jsonify({"token": jwt_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def verify_github_token(token):
    url = "https://api.github.com/user"

    response = requests.get(url, headers={"Authorization": f"token {token}"})

    if response.status_code == 200:
        data = response.json()
        user_info = {
            "id": data.get("id"),
            "name": data.get('name'),
            "login": data.get("login"),
            "avatar_url": data.get("avatar_url"),
        }
        return user_info
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
