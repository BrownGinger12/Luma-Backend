from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid
from decimal import Decimal

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
