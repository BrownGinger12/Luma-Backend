from flask import jsonify
from Model.review import Review
import jwt
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_review(request):
    try:
        review = Review(**request.json)
        response = review.create()
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({ "message": str(e)}), 500
    
def get_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        

        response = Review.get("review_id", review_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def update_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        review = Review.get("review_id", review_id)
        if review.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        response = Review.update(review_id, request.json)

        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def delete_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Review.delete(review_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str}), 500