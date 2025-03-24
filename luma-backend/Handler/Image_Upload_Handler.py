from flask import jsonify
from Gateways.S3_Gateway import S3Gateway
from Model.EventBridgeEvent import EventbridgeEvent
import json

s3_gateway = S3Gateway("luma-resources")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(request, item_id, item_type):
    """Handle image upload to S3."""
    # Check if file part is in request
    if 'user_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['user_file']

    if not item_id:
        return jsonify({"message": "No item ID provided"}), 400

    if item_type == "room":
        path = f"rooms/{item_id}"
    elif item_type == "user":
        path = f"user/{item_id}"
    elif item_type == "employee":
        path = f"employee/{item_id}"

    # Check if file has a valid extension
    if file and allowed_file(file.filename):
        
        filename = s3_gateway.upload_file_to_s3(file, path=path)

        if not filename:
            return jsonify({"message": "Failed to upload file to S3"}), 500
        
        if filename.get("statusCode") != 200:
            return jsonify({"message": filename.get("message")}), filename.get("statusCode")
        

        uploaded_file_name = f"https://{s3_gateway.bucket_name}.s3.amazonaws.com/{filename["file"]}"

        if item_type == "room":
            event = EventbridgeEvent("room_image_upload", json.dumps({"room_id": item_id, "image_url": uploaded_file_name}))
            event.send()
        elif item_type == "user":
            event = EventbridgeEvent("user_image_upload", json.dumps({"user_id": item_id, "image_url": uploaded_file_name}))
            event.send()
        elif item_type == "employee":
            event = EventbridgeEvent("employee_image_upload", json.dumps({"user_id": item_id, "image_url": uploaded_file_name}))
            event.send()

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "url": uploaded_file_name
        }), 200

    # File extension not allowed
    return jsonify({"message": "File extension not allowed"}), 400
