from pydantic import BaseModel


class AuthTokensResponse(BaseModel):
    access_token: str
    refresh_token: str
