from datetime import datetime

from pydantic import BaseModel


class ObjectData(BaseModel):
    year: int
    price: float
    CPU_model: str
    Hard_disk_size: str


class ObjectOutSchema(BaseModel):
    id: int
    name: str
    data: ObjectData


class ObjectInSchema(BaseModel):
    name: str
    data: ObjectData


class ObjectCreateOutSchema(BaseModel):
    id: int
    name: str
    data: ObjectData
    createdAt: datetime


class ObjectUpdateOutSchema(BaseModel):
    id: int
    name: str
    data: ObjectData
    updatedAt: datetime


class ObjectDeleteOutSchema(BaseModel):
    message: str
