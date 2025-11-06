"""Authentication schemas"""

from ninja import Schema


class UserRegistrationSchema(Schema):
    """Schema for user registration"""

    username: str
    password: str
    email: str = ""


class UserLoginSchema(Schema):
    """Schema for user login"""

    username: str
    password: str


class TokenResponseSchema(Schema):
    """Schema for token response"""

    access: str
    refresh: str
