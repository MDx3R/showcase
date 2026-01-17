from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    username: str
    password: str
