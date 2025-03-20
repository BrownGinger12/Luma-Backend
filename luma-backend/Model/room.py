from datetime import datetime 
from typing import List, Literal, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid
from decimal import Decimal


db_handler = DynamoDB("luma-rooms")

class Room(BaseModel):
    room_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique room id")
    room_name: str = Field(..., min_length=8, description="Room Name")
    room_type: Literal['single', 'double', 'twin', 'triple', 'quad', 'queen', 'king', 'deluxe', 'junior_suite', 'executive_suite', 'presidential_suite']
    room_description: str
    room_is_available: Optional[Annotated [bool, Field(..., description="Is the room available")]] 
    room_price: Decimal
    room_no_of_beds: int
    room_img_url: Optional[List[str]]
    room_is_guest_favorite: Optional[Annotated [bool, Field(..., description="Is the room a guest favorite")]]
    room_perks: Optional[List[str]]
    room_occupied_dates: Optional[List[str]] = Field(default=None)  # Changed to List[str]


    def create(self):
        try:
            room_data = self.__dict__
            # Convert datetime objects to ISO format strings
            if room_data.get('room_occupied_dates'):
                room_data['room_occupied_dates'] = [d.isoformat() if isinstance(d, datetime) else d 
                                                  for d in room_data['room_occupied_dates']]
            response = db_handler.put_item(room_data, {"room_id": room_data["room_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            room = db_handler.scan_table(attribute, atr_value)
            if room:
                # Convert ISO format strings back to datetime objects
                if room[0].get('room_occupied_dates'):
                    room[0]['room_occupied_dates'] = [datetime.fromisoformat(d) if isinstance(d, str) else d 
                                                    for d in room[0]['room_occupied_dates']]
                return {"statusCode": 200, "data": room[0]}

            return {"statusCode": 404, "message": "Room not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_some(attribute: str, atr_value: str):
        try:
            rooms = db_handler.scan_table_partial(attribute, atr_value)
            if rooms:
                return {"statusCode": 200, "data": rooms}

            return {"statusCode": 404, "message": "No rooms found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_all():
        try:
            rooms = db_handler.get_all_items()
            if rooms:
                return rooms

            return {"statusCode": 404, "message": "No rooms found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def update(room_id: str, update_data: dict):
        try:
            if "room_id" in update_data:
                return {"statusCode": 400, "message": "Room ID cannot be updated"}
            
            update_expression = "SET "
            expression_attribute_values = {}

            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value

            update_expression = update_expression.rstrip(", ")

            response = db_handler.update_item({"room_id": room_id}, update_expression, expression_attribute_values)

            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def delete(room_id: str):
        try:
            response = db_handler.delete_item({"room_id": room_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}




