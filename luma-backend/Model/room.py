from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid
from decimal import Decimal


db_handler = DynamoDB("luma-rooms")

class RoomTypes:
    single = 'single'
    double = 'double'
    twin = 'twin'
    triple = 'triple'
    quad = 'quad'
    queen = 'queen'
    king = 'king'
    deluxe = 'deluxe'
    junior_suite = 'junior_suite'
    executive_suite = 'executive_suite'
    presidential_suite = 'presidential_suite'

class Room(BaseModel):
    room_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique room id")
    room_name: str = Field(..., min_length=20, description="Room Name")
    room_type: RoomTypes
    room_description: str
    room_is_available: Optional[Annotated [bool, Field(..., description="Is the room available")]] 
    room_price: Decimal
    room_no_of_beds: int
    room_img_url: str


    def create(self):
        try:
            room_data = self.__dict__
            response = db_handler.put_item(room_data, {"room_id": room_data["room_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
    
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            room = db_handler.scan_table(attribute, atr_value)
            if room:
                return {"statusCode": 200, "data": room[0]}

            return {"statusCode": 404, "message": "Room not found"}
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
        
    
        
    
