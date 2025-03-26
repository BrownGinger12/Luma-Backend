from pydantic import BaseModel, Field   
from Gateways.DynamoDB_Gateway import DynamoDB
from passlib.context import CryptContext


db_handler = DynamoDB("luma-customer-accounts")

class User(BaseModel):
    user_id: str = Field(..., min_length=5, description="user_id cannot be empty")
    email: str = Field(..., description="Email cannot be empty")
    fullName: str = Field(..., min_length=5, description="Name cannot be empty")
    username: str = Field(..., min_length=6, description="Username cannot be empty")
    profile_url: str

    def create(self):
        try:

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


