from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

db_handler = DynamoDB("luma-reservation-transaction")

class Transaction(BaseModel):
    reservation_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique review id")
    user_id: str = Field(..., description="User id of the user who wrote the review")
    room_id: str = Field(..., description="Room id of the room being reviewed")
    event_id: Optional[Annotated [str, Field(..., description="Event id of the event")]]
    datestart: datetime = Field(..., description="Start date of the reservation")
    dateend: datetime = Field(..., description="End date of the reservation")
    payment_amount: float = Field(..., description="Payment amount")
    payment_type: str = Field(..., description="Payment type")
    description: str = Field(..., description="Description of the transaction")

    def create(self):
        try:
            transaction_data = self.__dict__
            response = db_handler.put_item(transaction_data, {"review_id": transaction_data["review_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            transaction = db_handler.scan_table(attribute, atr_value)
            if transaction:
                return {"statusCode": 200, "data": transaction[0]}

            return {"statusCode": 404, "message": "Transaction not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_all():
        try:
            transactions = db_handler.get_all_items()
            if transactions:
                return transactions
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def update(reservation_id: str, update_data: dict):
        try:
            if "reservation_id" in update_data:
                return {"statusCode": 400, "message": "Reservation ID cannot be updated"}
            
            update_expression = "SET "
            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
            
            update_expression = update_expression[:-2]
            response = db_handler.update_item(update_expression, {**update_data, "reservation_id": reservation_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def delete(reservation_id: str):
        try:
            response = db_handler.delete_item({"reservation_id": reservation_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
