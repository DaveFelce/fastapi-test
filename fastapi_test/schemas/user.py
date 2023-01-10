from pydantic import BaseModel, EmailStr


class GetUserResponseSchema(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class PostUserBodySchema(BaseModel):
    username: str
    email: EmailStr
