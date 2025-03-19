from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

class Transaction(BaseModel):
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique review id")
    user_id: str = Field(..., description="User id of the user who wrote the review")
    room_id: str = Field(..., description="Room id of the room being reviewed")
    event_id: Optional[Annotated [str, Field(..., description="Event id of the event")]]
    daterange: str = Field(..., description="Date range of the transaction")
    payment_amount: float = Field(..., description="Payment amount")
    payment_type: str = Field(..., description="Payment type")
    description: str = Field(..., description="Description of the transaction")
