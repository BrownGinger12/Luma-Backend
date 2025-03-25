import boto3
import botocore.exceptions
from werkzeug.utils import secure_filename

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
        try:
            self.s3_client.upload_fileobj(
                file,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file.content_type
                }
            )
        except botocore.exceptions.BotoCoreError as e:
            
            return {"statusCode": 500, "message": str(e)}

        return {"statusCode": 200, "file": s3_key}
