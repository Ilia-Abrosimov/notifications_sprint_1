from uuid import UUID

from pydantic import BaseModel, Field


class RegistrationBody(BaseModel):
    user_id: UUID = Field(title='user id, which was registered')
    email: str = Field(title='user email')


class RegistrationResponse(BaseModel):
    message: str = Field(title='response message')
