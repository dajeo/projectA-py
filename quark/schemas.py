from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    account_type: str
    token_type: str


class TokenData(BaseModel):
    tel: str | None = None


class UserResponse(BaseModel):
    id: int
    tel: str
    email: str
    type: int
    org: int


class UserInDb(UserResponse):
    password: str


class TaskResponse(BaseModel):
    workplace: str | None
    description: str
    files: str | None
