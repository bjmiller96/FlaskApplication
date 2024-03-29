from functools import wraps
from flask import request, jsonify
from models import User
import secrets, decimal, json

def token_required(flask_funciton):
    @wraps(flask_funciton)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'token is missing'}), 401
        
        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner = User.query.filter_by(token = token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'token is invalid'})
        return flask_funciton(current_user_token, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)