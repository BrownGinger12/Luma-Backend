from flask import jsonify
from Gateways.S3_Gateway import S3Gateway

s3_gateway = S3Gateway("luma-resources")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    if not filename or "." not in filename:
        return False
    return filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(request):
    """Handle image upload to S3."""
    # Check if file part is in request
    if 'user_file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['user_file']

    # Check if file has a valid extension
    if file and allowed_file(file.filename):
        filename = s3_gateway.upload_file_to_s3(file)

        if not filename:
            return jsonify({"message": "Failed to upload file to S3"}), 500

        return jsonify({
            "message": "File uploaded successfully",
            "filename": filename,
            "url": f"https://{s3_gateway.bucket_name}.s3.amazonaws.com/{filename["file"]}"
        }), 200

    # File extension not allowed
    return jsonify({"message": "File extension not allowed"}), 400
