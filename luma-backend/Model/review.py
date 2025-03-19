from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

db_handler = DynamoDB("luma-customer-reviews")

class Review(BaseModel):
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique review id")
    user_id: str = Field(..., description="User id of the user who wrote the review")
    room_id: str = Field(..., description="Room id of the room being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating of the room")
    is_accomodating: Optional[Annotated [bool, Field(..., description="Is the room accomodating")]]
    is_helpful_staff: Optional[Annotated [bool, Field(..., description="Is the staff helpful")]]
    is_cleanliness: Optional[Annotated [bool, Field(..., description="Is the room clean")]]
    is_comfortable: Optional[Annotated [bool, Field(..., description="Is the room comfortable")]]
    is_value_for_money: Optional[Annotated [bool, Field(..., description="Is the room value for money")]]
    is_quiet: Optional[Annotated [bool, Field(..., description="Is the room quiet")]]
    is_spacious: Optional[Annotated [bool, Field(..., description="Is the room spacious")]]
    review_text: Optional[Annotated [str, Field(..., description="Review text")]]

    def create(self):
        try:
            review_data = self.__dict__
            response = db_handler.put_item(review_data, {"review_id": review_data["review_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            review = db_handler.scan_table(attribute, atr_value)
            if review:
                return {"statusCode": 200, "data": review[0]}

            return {"statusCode": 404, "message": "Review not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def update(review_id: str, update_data: dict):
        try:
            if "review_id" in update_data:
                return {"statusCode": 400, "message": "Review ID cannot be updated"}
            
            update_expression = "SET "
            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
            
            update_expression = update_expression[:-2]
            response = db_handler.update_item({"review_id": review_id}, update_expression, update_data)
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def delete(review_id: str):
        try:
            response = db_handler.delete_item({"review_id": review_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}