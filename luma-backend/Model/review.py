from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from Gateways.DynamoDB_Gateway import DynamoDB
import uuid

class Room(BaseModel):
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