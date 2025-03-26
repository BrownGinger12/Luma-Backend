from pydantic import BaseModel, Field   
from Gateways.DynamoDB_Gateway import DynamoDB
from passlib.context import CryptContext
import uuid
import jwt
from datetime import datetime, timezone

db_handler = DynamoDB("luma-customer-accounts")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "I am a secret key"

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique user identifier")
    email: str = Field(..., description="Email cannot be empty")
    fullName: str = Field(..., min_length=5, description="Name cannot be empty")
    username: str = Field(..., min_length=6, description="Username cannot be empty")
    password: str = Field(..., min_length=6, description="Password cannot be empty and should be at least 6 characters long")
    profile_url: str


    def hash_password(self):
        """Hashes the password using bcrypt."""
        self.password = pwd_context.hash(self.password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifies a password against the stored hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create(self):
        try:
            self.hash_password()

            if db_handler.scan_table("username", self.username):
                return {"statusCode": 400, "message": "Username already exists"}
            
            user_data = self.dict()
            response = db_handler.put_item(user_data, {"user_id": user_data["user_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            user = db_handler.scan_table(attribute, atr_value)
            if user:
                return {"statusCode": 200, "data": user[0]}

            return {"statusCode": 404, "message": "User not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_all():
        try:
            users = db_handler.get_all_items()

            for user in users["data"]:
                user.pop("password")
                print (user)
            
            return users
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def update(user_id: str, update_data: dict):
        try:
            if "username" in update_data:
                if db_handler.scan_table("username", update_data["username"]):
                    return {"statusCode": 400, "message": "Username already exists"}
            
            if "email" in update_data:
                if db_handler.scan_table("email", update_data["email"]):
                    return {"statusCode": 400, "message": "Email already exists"}
            
            
            if "password" in update_data:
                update_data["password"] = pwd_context.hash(update_data["password"])

            update_expression = "SET "
            expression_attribute_values = {}

            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value

            update_expression = update_expression.rstrip(", ")

            print(user_id)
            response = db_handler.update_item(
                {"user_id": user_id},
                update_expression,
                expression_attribute_values
            )
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def delete(user_id: str):
        try:
            response = db_handler.delete_item({"user_id": user_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}


