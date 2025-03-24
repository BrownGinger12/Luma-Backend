from flask import jsonify
from Model.review import Review
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_review(request,user_id):
    data = request.json
    data["user_id"] = user_id

    try:
        review = Review(**data)
        response = review.create()

        if response.get("statusCode") == 400:
            return jsonify({"message": "Review already exists"}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": response.get("message")}), 500
        

        return jsonify(response), response.get("statusCode")
    except ValidationError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({ "message": str(e)}), 500
    
def get_review(review_id):
    try:
        data = review_id
        if not data:
            return jsonify({"message": response.get("message")}), 400
        

        response = Review.get("review_id", review_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        
        return jsonify(response), response.get("statusCode")
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_all_reviews():
    try:
        response = Review.get_all()

        if response.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        
        if response.get("data") == []:
            return jsonify({"message": "No reviews found"}), 404

        return jsonify(response), 200
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

        if response.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        if response.get("statusCode") == 400:
            return jsonify({"message": response.get("message")}), 400
        if response.get("statusCode") == 500:
            return jsonify({"message": response.get("message")}), 500

        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def delete_review(review_id):
    try:
        if not review_id:
            return jsonify({"message": "No data provided"}), 400
        
        response = Review.delete(review_id)

        if response.get("statusCode") == 404:
            return jsonify({"message": "Review not found"}), 404
        if response.get("statusCode") == 500:
            return jsonify({"message": response.get("message")}), 500
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str}), 500
    
def get_reviews_room(room_id):
    try:
        if not room_id:
            return jsonify({"message": "No data provided"}), 400
        
        response = Review.get_some(room_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500