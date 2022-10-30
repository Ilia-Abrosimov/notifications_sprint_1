import orjson
from app import spec
from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_pydantic_spec import Response
from schemas.auth import RegistrationBody, RegistrationResponse
from tools.broker import Rabbit
from tools.json_response import json_response
from tools.unpack import unpack_models

from messages.producers.api.models import SignUpMessage
from messages.schema.exchanges import exchanges
from messages.schema.queues import api_email_queues
from messages.schema.statuses import Statuses

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
rabbit = Rabbit(exchange_name=exchanges.API, queue_name=api_email_queues.SIGN_UP)


@auth_bp.route('/', methods=['POST'])
@spec.validate(
    body=RegistrationBody,
    resp=Response(HTTP_200=RegistrationResponse),
    tags=['AUTH']
)
@unpack_models
@json_response
# @jwt_required()
def auth(body: RegistrationBody) -> RegistrationResponse:
    """ User registration.
        ---
    """
    data = {'user_id': str(body.user_id),
            'email': str(body.email),
            'subject': 'Registration',
            'text': f'Hello by Team#8, please confirm registration go on to short link!'}
    message = SignUpMessage(content=data,
                            status=Statuses.PREPARED,
                            recipients=[str(body.user_id)])
    rabbit.send(message=orjson.dumps(message.dict()))
    return RegistrationResponse(message=f'Message with id = {message.id} sent to broker')
