from flask import jsonify
from Model.package import Package
import jwt
import datetime
from pydantic import ValidationError
from Gateways.DynamoDB_Gateway import DynamoDB

def add_package(request):
    try:
        package = Package(**request.json)
        response = package.create()
        return jsonify(response)
    except ValidationError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_package(request, package_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Package.get("package_id", package_id)
        if response.get("statusCode") == 404:
            return jsonify({"message": "Package not found"}), 404
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def get_all_packages(request):
    try:
        response = Package.get_all()

        if response.get("statusCode") == 404:
            return jsonify({"message": "Package not found"}), 404
        
        if response.get("data") == []:
            return jsonify({"message": "No packages found"}), 404
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
def update_package(request, package_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        package = Package.get("package_id", package_id)
        if package.get("statusCode") == 404:
            return jsonify({"Package not found"}), 404
        response = Package.update(package_id, request.json)

        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500

def delete_package(request, package_id):
    try:
        data = request
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        response = Package.delete(package_id)
        return jsonify(response)
    except Exception as e:
        return jsonify({"message": str(e)}), 500
