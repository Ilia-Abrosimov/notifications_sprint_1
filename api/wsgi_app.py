from gevent import monkey

monkey.patch_all()

# from app import app  # noqa

from app import create_app

app = create_app()
