from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import os
import uuid

db_handler = DynamoDB("luma-customer-accounts")

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique user identifier")
    fullName: str = Field(..., min_length=5, description="Name cannot be empty")
    username: str = Field(..., min_length=6, description="Username cannot be empty")
    password: str = Field(..., min_length=6, description="Password cannot be empty and should be at least 6 characters long")
    profile_url: str
    token: str

    def create(self):
        user_data = self.dict()
        response = db_handler.put_item(user_data, {"user_id": user_data["user_id"]})
        return response

