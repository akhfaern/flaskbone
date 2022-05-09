from flask import Flask, send_from_directory
from fb.lib.logger import FlaskBoneLogger
from flask_cors import CORS
from fb.auth_guard import AuthGuard
import json


def create_app():
    _ = FlaskBoneLogger()

    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.wsgi_app = AuthGuard(app.wsgi_app)
    app.config.from_file("config.json", load=json.load)
    # create_directories(app.config)

    from . import generic_blue_print, auth
    app.register_blueprint(generic_blue_print.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    @app.route('/favicon.ico')
    def send_favicon():
        return app.send_static_file('favicon.ico')

    @app.route('/static/js/<filename>')
    def send_js(filename):
        return send_from_directory(app.config['CLIENT_STATIC_JS'], filename)

    @app.route('/static/css/<filename>')
    def send_css(filename):
        return send_from_directory(app.config['CLIENT_STATIC_CSS'], filename)

    @app.route('/static/media/<filename>')
    def send_media(filename):
        return send_from_directory(app.config['CLIENT_STATIC_MEDIA'], filename)

    @app.route('/assets/<path:filename>')
    def send_assets(filename):
        return send_from_directory(app.config['STATIC_ASSETS'], filename)

    return app
