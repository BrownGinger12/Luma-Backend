from decimal import Decimal
from flask import jsonify
from Model.room import Room
from Helper.helper_func import *
import jwt
from Model.EventBridgeEvent import EventbridgeEvent
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_room(request):
    try:
        room = Room(**request.json)
        response = room.create()

        if response.get("statusCode") == 400:
            return jsonify({"message": "Room already exists"}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
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
        
        if response.get("data") == []:
            return jsonify({"message": "No rooms found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def search_rooms(request, attribute, atr_value):
    try:
        response = Room.get_some(attribute, atr_value)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404
        
        if response.get("data") == []:
            return jsonify({"message": "No rooms found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
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
        update_data = request.json.copy()

        # Convert any datetime objects in room_occupied_dates to strings
        if "room_occupied_dates" in update_data and update_data["room_occupied_dates"]:
            update_data["room_occupied_dates"] = [
                d.strftime("%Y-%m-%d") if isinstance(d, datetime.datetime)
                else d if isinstance(d, str)
                else datetime.datetime.fromtimestamp(d).strftime("%Y-%m-%d")
                for d in update_data["room_occupied_dates"]
            ]

        room = Room(**room_data)
        room.__dict__.pop("room_id")
        room.__dict__.update(update_data)
        room.__dict__["room_price"] = Decimal(str(room.__dict__["room_price"]))

        response = Room.update(room_id, room.__dict__)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Room not found"}), 404
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        

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
    
def update_room_dates(event, context):
    try:
        print(event)
         
        if 'detail' in event:
            body = event['detail']
            date_start = body['reservation_date_start'].split('T')[0]
            date_end = body['reservation_date_end'].split('T')[0]
            dates = get_dates_in_range(date_start, date_end)

            room = Room.get("room_id", body['room_id'])
            room_dates = room.get("data")['room_occupied_dates']
            room_dates.extend(dates)
            
            response = Room.update(body['room_id'], {"room_occupied_dates": room_dates})

            if response.get("statusCode") == 404:
                return {"message": "Room not found"}, 404
            if response.get("statusCode") == 500:
                return {"message": "Internal server error"}, 500
            
            return response
        
    except ValueError as e:
        event = EventbridgeEvent(
            "transaction_on_failure",
            {"message": str(e), "reservation_id": body["reservation_id"]}
        )
        event.send()
        return {"message": e}
    
def update_room_image(event, context):
    try:
        print(event)
         
        if 'detail' in event:
            body = event['detail']
            room_id = body['room_id']
            file_url = body['image_url']

            room = Room.get("room_id", room_id)
            room_image = room.get("data")['room_img_url']
            room_image.append(file_url)
            
            response = Room.update(room_id, {"room_img_url": room_image})

            if response.get("statusCode") == 404:
                return {"message": "Room not found"}, 404
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