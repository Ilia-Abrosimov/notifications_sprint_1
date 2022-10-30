from core.config import settings
from extensions import jwt
from flask import Flask, request
from flask_pydantic_spec import FlaskPydanticSpec

spec = FlaskPydanticSpec('flask', title='API', version=settings.api_version, path=settings.swagger_path)


def create_app():
    from v1.auth import auth_bp
    from v1.review_likes import review_likes_bp
    app = Flask(__name__)
    app.register_blueprint(review_likes_bp)
    app.register_blueprint(auth_bp)
    app.config['JWT_SECRET_KEY'] = settings.jwt_secret_key

    # @app.before_request
    # def before_request():
    #     request_id = request.headers.get('X-Request-Id')
    #     if not request_id:
    #         raise RuntimeError('request id is required')

    jwt.init_app(app)
    spec.register(app)

    return app
