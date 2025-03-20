from decimal import Decimal
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
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

def get_room(request, room_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        

        response = Room.get("room_id", room_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_all_rooms(request):
    try:
        response = Room.get_all()
        
        if response.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def search_rooms(request, attribute, atr_value):
    try:
        response = Room.get_some(attribute, atr_value)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def update_room(request, room_id):
    try:
        data = request 
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        room = Room.get("room_id", room_id)
        if room.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404
        
        room_data = room.get("data")

        room = Room(**room_data)

        room.__dict__.pop("room_id")

        room.__dict__.update(request.json)

        room.__dict__["room_price"] = Decimal(str(room.__dict__["room_price"]))

        response = Room.update(room_id, room.__dict__)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": f"{str(e)}"}), 500
    
def delete_room(request, room_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Room.delete(room_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500