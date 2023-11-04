from fastapi import Form
from pydantic import BaseModel


class UserDTO(BaseModel):
    name: str
    age: int
    city: str
