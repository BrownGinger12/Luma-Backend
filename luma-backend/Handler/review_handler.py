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
        return jsonify({"statusCode": 400, "message": str(e)})
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def get_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        

        response = Review.get("review_id", review_id)
        if response.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Review not found"})
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def update_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        review = Review.get("review_id", review_id)
        if review.get("statusCode") == 404:
            return jsonify({"statusCode": 404, "message": "Review not found"})
        response = Review.update(review_id, request.json)

        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str(e)})
    
def delete_review(request, review_id):
    try:
        data = request
        if not data:
            return jsonify({"statusCode": 400, "message": "No data provided"})
        
        response = Review.delete(review_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"statusCode": 500, "message": str})