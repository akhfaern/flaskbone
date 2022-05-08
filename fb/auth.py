from flask import Blueprint, request, Response
from fb.lib.user_management import UserManagement
import time
import json
import uuid
from fb.lib.logger import FlaskBoneLogger

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['POST'])
def login():
    mlogger = FlaskBoneLogger.get_logger("flaskbone")
    req = request.get_json()
    username = req.get("username", "").strip()
    password = req.get("password", "").strip()
    if len(username) > 1 and len(password) > 1:
        user_management = UserManagement()
        user = user_management.get_user_by_username_with_password(username)
        if user is None:
            mlogger.error("User Login error: {0} not found".format(username))
            return Response(json.dumps({'error': 'incorrect_user_pass'}), mimetype='application/json')
        if user.get('active') is not True:
            mlogger.error("User Login error: {0} is passive".format(username))
            return Response(json.dumps({'error': 'incorrect_user_pass'}), mimetype='application/json')
        if password == user.get('password'):
            user["refreshToken"] = str(uuid.uuid4())
            user_management.config_manager.write_config()
            mlogger.info("User Login success: {0}".format(username))
            result = {
                'errorCode': 0,
                'refreshToken': user.get('refreshToken'),
                'token': UserManagement.encode({
                    'name': user.get('fullname'),
                    'username': user.get('username'),
                    'userType': user.get('userType'),
                    'refreshToken': user.get('refreshToken'),
                    'exp': int(time.time()) + 7200
                })
            }
            return Response(json.dumps(result), mimetype='application/json')
        else:
            mlogger.error("User Login error: {0} wrong password".format(username))
    return Response(json.dumps({'error': 'incorrect_user_pass'}), mimetype='application/json')


@bp.route('/refreshToken', methods=['POST'])
def refresh_token():
    req = request.get_json()
    user_management = UserManagement()
    user_refresh_token = req.get('refreshToken', '')
    user = user_management.get_user_by_refresh_token(user_refresh_token)
    if user is not None:
        user["refreshToken"] = str(uuid.uuid4())
        user_management.config_manager.write_config()
        new_token = {
            'errorCode': 0,
            'refreshToken': user.get('refreshToken'),
            'token': UserManagement.encode({
                'name': user.get('fullname'),
                'username': user.get('username'),
                'userType': user.get('userType'),
                'refreshToken': user.get('refreshToken'),
                'exp': int(time.time()) + 7200
            }),
        }
        return Response(json.dumps(new_token), mimetype='application/json')
    return Response(json.dumps({'error': 'incorrect_refresh_token'}), mimetype='application/json')