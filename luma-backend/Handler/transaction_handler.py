from flask import jsonify
from Model.transaction import Transaction
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB
from decimal import Decimal

def add_transaction(request, user_id):
    try:
        transaction = Transaction(**request.json, user_id=user_id)
        response = transaction.create()
        if response.get("statusCode") == 400:
            return jsonify({"message": "Transaction already exists"}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
        return jsonify(response), response.get("statusCode")
    except ValidationError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_transaction(request, reservation_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        

        response = Transaction.get("reservation_id", reservation_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Transaction not found"}), 404
        
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_all_transactions(request): 
    try:
        response = Transaction.get_all()
        
        if response.get("statusCode") == 404:
            return jsonify({"message": "Transaction not found"}), 404
        
        if response.get("data") == []:
            return jsonify({"message": "No transactions found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def update_transaction(request, reservation_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        transaction = Transaction.get("reservation_id", reservation_id)
        if transaction.get("statusCode") == 404:
            return jsonify({"message": "Transaction not found"}), 404

        # Convert payment_amount to Decimal if present
        update_data = request.json.copy()
        if "payment_amount" in update_data:
            update_data["payment_amount"] = Decimal(str(update_data["payment_amount"]))

        response = Transaction.update(reservation_id, update_data)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Transaction not found"}), 404
        if response.get("statusCode") == 400:
            return jsonify({"message": "Transaction ID cannot be updated"}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def delete_transaction(request, reservation_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Transaction.delete(reservation_id)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Transaction not found"}), 404
        
        if response.get("statusCode") == 500:
            return jsonify({"message": "Internal server error"}), 500
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def delete_transaction_event(event, context):
    try:
        if 'detail' in event:
            body = event['detail']
            reservation_id = body['reservation_id']
            response = Transaction.delete(reservation_id)
            return response
        
        return {"statusCode": 400, "message": "No reservation"}
    
    except Exception as e:
        return {"statusCode": 500, "message": str(e)}
