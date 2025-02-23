from pydantic import BaseModel, EmailStr, constr

class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PostRequest(BaseModel):
    text: constr(max_length=1048576)

class PostResponse(BaseModel):
    id: int
    text: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"