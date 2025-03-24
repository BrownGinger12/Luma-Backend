from datetime import datetime
from decimal import Decimal
from typing import Optional, Literal
from Model.EventBridgeEvent import EventbridgeEvent
from Helper.helper_func import DecimalEncoder
import json
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

db_handler = DynamoDB("luma-reservation-transaction")

class Transaction(BaseModel):
    reservation_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique reservation id")
    user_id: str = Field(..., description="User id of the user who wrote the review")
    room_id: str = Field(..., description="Room id of the room being reviewed")
    reservation_event_id: Optional[str] = Field(default=None, description="Event id of the event")
    reservation_date_start: datetime = Field(..., description="Start date of the reservation")
    reservation_date_end: datetime = Field(..., description="End date of the reservation")
    reservation_payment_amount: Decimal = Field(..., description="Payment amount")
    reservation_payment_type: str = Field(..., description="Payment type")
    reservation_description: str = Field(..., description="Description of the transaction")
    reservation_status:  Literal['pending', 'active', 'completed', 'cancelled']

    def create(self):
        try:
            transaction_data = self.model_dump()
            # Convert Decimal to string for DynamoDB
            transaction_data['reservation_payment_amount'] = str(transaction_data['reservation_payment_amount'])
            # Convert datetime objects to ISO format strings
            transaction_data['reservation_date_start'] = transaction_data['reservation_date_start'].isoformat()
            transaction_data['reservation_date_end'] = transaction_data['reservation_date_end'].isoformat()
            
            response = db_handler.put_item(transaction_data, {"reservation_id": transaction_data["reservation_id"]})
            
            if response.get("statusCode") == 200:
                event = EventbridgeEvent("transaction_update_room_dates", json.dumps(transaction_data, cls=DecimalEncoder))
                event.send()

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
            expression_attribute_values = {}

            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value

            update_expression = update_expression.rstrip(", ")
            response = db_handler.update_item({"reservation_id": reservation_id}, update_expression, expression_attribute_values)
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
