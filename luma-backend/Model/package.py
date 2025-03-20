from decimal import Decimal
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

db_handler = DynamoDB("luma-package")

class Package(BaseModel):
    package_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique package id")
    package_name: str = Field(..., min_length=8, description="Package Name")
    package_description: str
    package_price: Decimal
    room_id: str = Field(..., description="Room id of the room in the package")
    event_id: Optional[str] = Field(default=None, description="Event id of the event")

    def create(self):
        try:
            package_data = self.__dict__
            response = db_handler.put_item(package_data, {"package_id": package_data["package_id"]})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get(attribute: str, atr_value: str):
        try:
            package = db_handler.scan_table(attribute, atr_value)
            if package:
                return {"statusCode": 200, "data": package[0]}

            return {"statusCode": 404, "message": "Package not found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def get_all():
        try:
            packages = db_handler.get_all_items()
            if packages:
                return packages

            return {"statusCode": 404, "message": "No packages found"}
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def update(package_id: str, update_data: dict):
        try:
            if "package_id" in update_data:
                return {"statusCode": 400, "message": "Package ID cannot be updated"}
            
            update_expression = "SET "
            for key, value in update_data.items():
                update_expression += f"{key} = :{key}, "
            
            update_expression = update_expression[:-2]
            response = db_handler.update_item({"package_id": package_id}, update_expression, update_data)
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
        
    @staticmethod
    def delete(package_id: str):
        try:
            response = db_handler.delete_item({"package_id": package_id})
            return response
        except Exception as e:
            return {"statusCode": 500, "message": str(e)}
