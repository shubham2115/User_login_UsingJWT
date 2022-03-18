from flask import request
import datetime
import jwt
from functools import wraps
from flask import jsonify

secret = "thisisasecretkey"

token_dict = {}


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        if 'access-token' in request.headers:
            short_token = request.headers.get('access-token')
        else:
            short_token = request.args.get('token')
        token = token_dict[int(short_token)]
        if not token:
            return jsonify(message='Token is missing!')
        # try:
        data = jwt.decode(token,secret,algorithms=["HS256"])
        # except:
        #     return jsonify(message='Token is invalid')

        return f(data['User'])
    return decorated


def get_token(UserName):
    import app
    token = jwt.encode({'User': UserName, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=600))},
                       app.app.config['SECRET_KEY'])
    return token


def url_short(token):
    key = len(token_dict) + 1
    token_dict.__setitem__(key, token)
    return key


