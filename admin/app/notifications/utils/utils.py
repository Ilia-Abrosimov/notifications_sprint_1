from pydantic import UUID4, BaseModel, EmailStr


class EmailValidator(BaseModel):
    emails: list[EmailStr]


class UUID4Validator(BaseModel):
    uuids: list[UUID4]
