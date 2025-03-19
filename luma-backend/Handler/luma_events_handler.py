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
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"statusCode": 400, "message": str(e)})
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def get_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        

        response = Event.get("event_id", event_id)
        if response.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Event not found"})
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def  update_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        event = Event.get("event_id", event_id)
        if event.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Event not found"})
        response = Event.update(event_id, request.json)

        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})

def delete_event(request, event_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        response = Event.delete(event_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})