from decimal import Decimal
from typing import Optional, List
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

db_handler = DynamoDB("luma-events")

class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique event id")
    event_description: str = Field(..., description="Event description")
    event_price: Decimal
    event_dates: Optional[List[str]] = Field(default=None)


    def create(self):
        try:
            event_data = self.__dict__
            response = db_handler.put_item(event_data, {"event_id": event_data["event_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            event = db_handler.scan_table(attribute, atr_value)
            if event:
                return {"statusCode": 200, "data": event[0]}

            return {"statusCode": 404, "message": "Event not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_all():
        try:
            events = db_handler.get_all_items()
            if events:
                return events

            return {"statusCode": 404, "message": "No events found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def update(event_id: str, update_data: dict):
        try:
            if "event_id" in update_data:
                return {"statusCode": 400, "message": "Event ID cannot be updated"}
            
            update_expression = "SET "
            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
            
            update_expression = update_expression[:-2]
            response = db_handler.update_item({"event_id": event_id}, update_expression, update_data)
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def delete(event_id: str):
        try:
            response = db_handler.delete_item({"event_id": event_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}