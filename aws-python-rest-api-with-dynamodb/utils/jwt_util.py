import datetime
import os

import jwt

ALGORITHM = 'HS256'


def create_jwt_token(username):
    expiration = datetime.datetime.now() + datetime.timedelta(hours=5)
    token = jwt.encode(
        {'sub': username, 'exp': expiration},
        os.environ["SECRET_KEY"],
        algorithm=ALGORITHM
    )
    return token
