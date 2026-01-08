from pydantic import BaseModel


class EnrollRequest(BaseModel):
    email: str
    full_name: str
    phone: str | None = None
    message: str | None = None
    user_id: str | None = None
