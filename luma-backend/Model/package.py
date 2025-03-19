from decimal import Decimal
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

class Package(BaseModel):
    package_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique package id")
    package_name: str = Field(..., min_length=20, description="Package Name")
    package_description: str
    package_price: Decimal
    room_id: str = Field(..., description="Room id of the room in the package")
    event_id: Optional[Annotated [str, Field(..., description="Event id of the event in the package")]]
