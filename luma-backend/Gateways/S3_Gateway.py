import boto3
import botocore.exceptions
from werkzeug.utils import secure_filename
import base64

class S3Gateway:
    def __init__(self, bucket_name):
        """Initialize the S3 client with a specified bucket and region."""
        self.s3_client = boto3.client("s3", region_name="us-east-2")
        self.bucket_name = bucket_name
        
    def upload_file_to_s3(self, file, path, acl="public-read"):
        """Uploads a file to the specified S3 bucket."""
        filename = secure_filename(file.filename)

        if not path:
            return {"statusCode": 400, "message": "Folder name not provided"}
        
        filename = secure_filename(file.filename)

        # Construct full S3 key (folder/filename)
        s3_key = f"{path}/{filename}"
        print(file.content_type)
        
        try:
            # Read file content and encode it in Base64
            encoded_data = base64.b64encode(file.read())
            
            # Upload encoded file to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=encoded_data,
                ACL=acl,
                ContentType=file.content_type
            )
        except botocore.exceptions.BotoCoreError as e:
            return {"statusCode": 500, "message": str(e)}

        return {"statusCode": 200, "file": s3_key}

