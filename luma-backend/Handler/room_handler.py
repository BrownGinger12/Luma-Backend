from flask import jsonify
from Model.room import Room
import jwt
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_room(request):
    try:
        room = Room(**request.json)
        response = room.create()
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"statusCode": 400, "message": str(e)})
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    

def get_room(request, room_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        

        response = Room.get("room_id", room_id)
        if response.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Room not found"})
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def update_room(request, room_id):
    try:
        data = request 
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        room = Room.get("room_id", room_id)
        if room.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Room not found"})
        

        response = Room.update(room_id, request.json)
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def delete_room(request, room_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        response = Room.delete(room_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})