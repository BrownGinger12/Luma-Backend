from flask import jsonify
from Model.event import Event
import jwt
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_event(request):
    try:
        event = Event(**request.json)
        response = event.create()
        if response.get("statusCode") == 400:
            return jsonify({"message": "Event already exists"}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        return jsonify(response)
    
    except ValidationError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Event.get("event_id", event_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Event not found"}), 404
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_all_events(request):
    try:
        response = Event.get_all()

        if response.get("statusCode") == 404:
            return jsonify({"message": "Event not found"}), 404
        if response.get("data") == []:
            return jsonify({"message": "No events found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def update_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        event = Event.get("event_id", event_id)
        if event.get("statusCode") == 404:
            return jsonify({"Event not found"}), 404
        response = Event.update(event_id, request.json)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Event not found"}), 404
        
        if response.get("statusCode") == 400:
            return jsonify({"message": "Event ID cannot be updated"}), 400
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500

        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Event.delete(event_id)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Event not found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500