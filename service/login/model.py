
import pydantic


class User(pydantic.BaseModel):
    email: str
    password: str