from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel, Field


class LikeType(IntEnum):
    like = 1
    dislike = 0


class LikeReviewBody(BaseModel):
    user_id: UUID = Field(title='user id, which was rated review')
    review_id: UUID = Field(title='review id, which was rated')
    value: LikeType = Field(title='review rating')


class LikeReviewResponse(BaseModel):
    message: str = Field(title='response message')
