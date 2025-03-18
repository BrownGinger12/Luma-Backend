from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
from passlib.context import CryptContext
import uuid

db_handler = DynamoDB("luma-customer-accounts")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique user identifier")
    fullName: str = Field(..., min_length=5, description="Name cannot be empty")
    username: str = Field(..., min_length=6, description="Username cannot be empty")
    password: str = Field(..., min_length=6, description="Password cannot be empty and should be at least 6 characters long")
    profile_url: str
    token: str

    def hash_password(self):
        """Hashes the password using bcrypt."""
        self.password = pwd_context.hash(self.password)

    def verify_password(self, plain_password: str) -> bool:
        """Verifies a password against the stored hash."""
        return pwd_context.verify(plain_password, self.password)

    def create(self):
        self.hash_password()

        if db_handler.scan_table("username", self.username):
            return {"statusCode": 400, "message": "Username already exists"}
        
        user_data = self.dict()
        response = db_handler.put_item(user_data, {"user_id": user_data["user_id"]})
        return response

