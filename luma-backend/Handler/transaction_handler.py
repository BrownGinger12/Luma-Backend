from flask import jsonify
from Model.transaction import Transaction
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_transaction(request):
    try:
        transaction = Transaction(**request.json)
        response = transaction.create()
        return jsonify(response)
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
        response = Transaction.update(reservation_id, request.json)

        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def delete_transaction(request, reservation_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Transaction.delete(reservation_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    