from pydantic import BaseModel
from typing import *
import datetime as dt


class GeneratedSchema1(BaseModel):
    id: int


class GeneratedSchema2(BaseModel):
    id: int
    colors: Optional[List[str]]
    numbers: List[int] = [1, 2, 3]
    text: str = "default_string"
    date: dt.date = "2020-04-20"
    dt_: dt.datetime = "2020-04-20 09:30"
    time: dt.time = "09:30"
    other_schema: GeneratedSchema1

    class Config:
        orm_mode = True
