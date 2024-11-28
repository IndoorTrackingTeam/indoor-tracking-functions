from typing import Annotated, List, Optional
from pydantic import BaseModel, BeforeValidator, Field
from datetime import datetime

PyObjectId = Annotated[str, BeforeValidator(str)]

class EquipmentCurrentDateAndRoom(BaseModel):
    name: str = Field(...)
    register_: str = Field(alias="register")
    c_room: str = Field(...)
    c_date: datetime = Field(...)

class UpdateEquipmentsHistoric(BaseModel):
    esp_id: str = Field(...)
    room: str = Field(...)
    initial_date: datetime = Field(...)

class UpdateEquipmentsCurrentRoom(BaseModel):
    esp_id: str = Field(...)
    c_room: str = Field(...)

class NotificationBody(BaseModel):
    equipment_name: str = Field(...)
    register_: str = Field(...)
    date: datetime = Field(...)
    location: str = Field(...)
