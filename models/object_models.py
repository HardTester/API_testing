from typing import List

from pydantic import BaseModel, Field


class ObjectData(BaseModel):
    year: int
    price: float
    cpu_model: str = Field(alias="CPU model")
    hard_disk_size: str = Field(alias="Hard disk size")


class CustomObj(BaseModel):
    name: str


class CustomObjData(BaseModel):
    bool: bool
    int: int
    float: float
    string: str
    array: List[str]
    obj: CustomObj


class ObjectOutSchema(BaseModel):
    id: str
    name: str
    data: ObjectData


class ObjectCreateOutSchema(BaseModel):
    id: str
    name: str | None
    data: ObjectData | None
    createdAt: str


class CustomObjCreateOutSchema(BaseModel):
    id: str
    name: str
    data: CustomObjData
    createdAt: str


class ObjectUpdateOutSchema(BaseModel):
    id: str
    name: str | None
    data: ObjectData | None
    updatedAt: str


class CustomObjUpdateOutSchema(BaseModel):
    id: str
    name: str
    data: CustomObjData
    updatedAt: str
