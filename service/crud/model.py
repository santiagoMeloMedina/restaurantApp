from typing import List
import pydantic
import enum


class CommonModel(pydantic.BaseModel):
    owner: str
    public: bool


class Days(enum.Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class Schedule(pydantic.BaseModel):
    open: str
    close: str
    days: List[Days]

    class Config:
        use_enum_values = True


class Restaurant(CommonModel):
    id: str
    name: str
    category: str
    schedule: Schedule
    rate: int
