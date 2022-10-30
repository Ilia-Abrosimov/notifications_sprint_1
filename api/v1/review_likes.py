import asyncio

import orjson
from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from schemas.review_likes import LikeReviewBody, LikeReviewResponse
from tools.broker import Rabbit
from tools.json_response import json_response
from tools.unpack import unpack_models

from messages.producers.api.models import ReviewLikeMessage
from messages.schema.exchanges import exchanges
from messages.schema.queues import api_email_queues
from messages.schema.statuses import Statuses

review_likes_bp = Blueprint('review_likes', __name__, url_prefix='/api/v1/review_likes')
rabbit = Rabbit(exchange_name=exchanges.API, queue_name=api_email_queues.REVIEW_LIKE)


@review_likes_bp.route('/', methods=['POST'])
@spec.validate(
    body=LikeReviewBody,
    resp=Response(HTTP_200=LikeReviewResponse),
    tags=['UGC']
)
@unpack_models
@json_response
# @jwt_required()
def create_like(body: LikeReviewBody) -> LikeReviewResponse:
    """ Like/dislike review.
        ---
    """
    data = {'user_id': str(body.user_id),
            'review_id': str(body.review_id),
            'value': body.value,
            }
    message = ReviewLikeMessage(content=data,
                                status=Statuses.PREPARED,
                                recipients=[str(body.user_id)])
    rabbit.send(message=orjson.dumps(message.dict()))
    return LikeReviewResponse(message=f'Message with id = {message.id} sent to broker')
