from werkzeug.wrappers import Request, Response
from fb.lib.user_management import UserManagement
import time


class AuthGuard:
    def __init__(self, app):
        self.app = app
        self.debug = False

    def __call__(self, environ, start_response):
        request = Request(environ)
        url = request.path
        method = request.method
        if method == 'OPTIONS':
            return self.app(environ, start_response)
        if self.debug:
            print(url, method)
        if url not in ['/auth/login', '/', '/favicon.ico'] and url[0:7] not in ['/static', '/assets']:
            auth = request.headers.get('Authorization')
            if self.debug:
                print('Auth', auth[7:])
            if auth is None:
                res = Response(u'Authorization failed', mimetype='text/plain', status=401)
                return res(environ, start_response)
            else:
                try:
                    user = UserManagement()
                    authuser = user.decode(auth[7:])
                    n = int(time.time())
                    expire = authuser.get('exp')
                    if n > expire:
                        res = Response(u'Token expired', mimetype='text/plain', status=401)
                        return res(environ, start_response)
                    if authuser is not None and \
                            user.get_user_by_username_with_password(authuser.get('username')) is not None:
                        return self.app(environ, start_response)
                    res = Response(u'Permission failed', mimetype='text/plain', status=403)
                    return res(environ, start_response)
                except Exception as e:
                    print(e)
                    res = Response(u'Authorization failed', mimetype='text/plain', status=401)
                    return res(environ, start_response)
        return self.app(environ, start_response)
