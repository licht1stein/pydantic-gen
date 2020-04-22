from pydantic import BaseModel
from typing import *


class GeneratedSchema1(BaseModel):
    id: int


class GeneratedSchema2(BaseModel):
    id: int
    colors: Optional[List[str]]
    numbers: List[int] = [1, 2, 3]
    text: str = 'default_string'
    other_schema: GeneratedSchema1

    class Config:
        orm_mode = True
