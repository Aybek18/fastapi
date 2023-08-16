from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    phone_number: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    firebase_token: str


class UserRetrieve(UserBase):
    id: int
    photo_url: str | None = None
    is_active: bool


class UserRetrieveWithToken(UserRetrieve):
    access_token: str
    refresh_token: str


class UserUpdate(BaseModel):
    username: str | None = None
    phone_number: str | None = None
    photo_url: str | None = None

    class Config:
        orm_mode = True


class UserRegistrationStatus(BaseModel):
    is_registered: bool


class Token(BaseModel):
    access_token: str
    token_type: str
