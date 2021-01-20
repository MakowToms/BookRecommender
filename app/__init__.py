import os
from datetime import datetime

from beaker.cache import CacheManager
from beaker.middleware import SessionMiddleware
from beaker.util import parse_cache_config_options
from celery import Celery
from flask import Flask, render_template
from flask.sessions import SessionInterface
from flask_migrate import Migrate

# Instantiate Flask extensions
migrate = Migrate()


def get_config():
    # Instantiate Flask
    app = Flask(__name__)

    # Load App Config settings
    # Load common settings from 'app/settings.py' file
    app.config.from_object('app.settings')
    # Load local settings from environmental variable
    if 'APPLICATION_SETTINGS' in os.environ:
        app.config.from_envvar(os.environ['APPLICATION_SETTINGS'])
    # Load extra config settings from the AWS Secrets Manager
    if 'AWS_SECRETS_MANAGER_CONFIG' in os.environ:
        secret_config = get_secrets(os.environ['AWS_SECRETS_MANAGER_CONFIG'])
        app.config.update(secret_config)
    elif 'AWS_SECRETS_MANAGER_CONFIG' in app.config:
        secret_config = get_secrets(app.config['AWS_SECRETS_MANAGER_CONFIG'])
        app.config.update(secret_config)
    # Load extra config settings from environment- note that the config key must exist in app.config to get picked up
    for setting in app.config:
        if setting in os.environ:
            if os.environ[setting].lower() == 'true':
                app.config[setting] = True
            elif os.environ[setting].lower() == 'false':
                app.config[setting] = False
            else:
                app.config[setting] = os.environ[setting]
    # Apply any config transformations here.
    if app.config.get('USER_LDAP', False):
        app.config['USER_ENABLE_USERNAME'] = True
    return app.config


# We need the base configuration to setup services before the app is created.
base_config = get_config()

# Initiate Services
celery = Celery(__name__, broker=base_config['CELERY_BROKER'])
cache = None # Initiate below, but define here for scope reasons.


def create_app(extra_config_settings={}):
    """Create a Flask applicaction.
    """
    # Instantiate Flask
    app = Flask(__name__)

    # Load extra config settings from 'extra_config_settings' param
    base_config = get_config()
    app.config.update(base_config)
    # Load extra config settings from 'extra_config_settings' param
    app.config.update(extra_config_settings)

    # Setup Session Manager
    init_session_manager(app)

    # Setup Celery
    init_celery_service(app)

    # Add HTTP Error pages
    init_error_handlers(app)

    # Register blueprints
    from app.extensions.jinja import jinja_extensions_blueprint
    app.register_blueprint(jinja_extensions_blueprint)
    app.jinja_env.globals.update(now=datetime.utcnow)

    from app.views.misc_views import main_blueprint
    app.register_blueprint(main_blueprint)

    # Setup an error-logger to send emails to app.config.ADMINS
    if app.config.get('EMAIL_ERRORS', False):
        init_email_error_handler(app)

    return app


def init_cache_manager(app):
    cache_opts = {'cache.expire': app.config.get('CACHE_EXPIRE', 3600)}

    if 'CACHE_TYPE' not in app.config or not app.config['CACHE_TYPE']:
        app.config['CACHE_TYPE'] = 'file'

    if app.config['CACHE_TYPE'] == 'file':
        if 'CACHE_ROOT' not in app.config or not app.config['CACHE_ROOT']:
            app.config['CACHE_ROOT'] = '/tmp/%s' % __name__

    cache_opts['cache.type'] = app.config['CACHE_TYPE']

    if 'CACHE_ROOT' in app.config and app.config['CACHE_ROOT']:
        cache_opts['cache.data_dir'] = app.config['CACHE_ROOT'] + '/data'
        cache_opts['cache.lock_dir'] = app.config['CACHE_ROOT'] + '/lock'

    if 'CACHE_URL' in app.config and app.config['CACHE_URL']:
        cache_opts['cache.url'] = app.config['CACHE_URL']


    cache = CacheManager(**parse_cache_config_options(cache_opts))


def init_session_manager(app):
    session_opts = {'cache.expire': 3600}

    if 'CACHE_TYPE' not in app.config or not app.config['CACHE_TYPE']:
        app.config['CACHE_TYPE'] = 'file'

    if app.config['CACHE_TYPE'] == 'file':
        if 'CACHE_ROOT' not in app.config or not app.config['CACHE_ROOT']:
            app.config['CACHE_ROOT'] = '/tmp/%s' % __name__

    session_opts['session.type'] = app.config['CACHE_TYPE']

    if 'CACHE_ROOT' in app.config and app.config['CACHE_ROOT']:
        session_opts['session.data_dir'] = app.config['CACHE_ROOT'] + '/session'

    if 'CACHE_URL' in app.config and app.config['CACHE_URL']:
        session_opts['session.url'] = app.config['CACHE_URL']

    session_opts['session.auto'] = app.config.get('SESSION_AUTO', True)
    session_opts['session.cookie_expires'] = app.config.get('SESSION_COOKIE_EXPIRES', 86400)
    session_opts['session.secret'] = app.secret_key

    class BeakerSessionInterface(SessionInterface):
        def open_session(self, app, request):
            session = request.environ['beaker.session']
            return session

        def save_session(self, app, session, response):
            session.save()

    app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
    app.session_interface = BeakerSessionInterface()


def init_celery_service(app):
    celery.conf.update(app.config)


def init_error_handlers(app):

    def show_error(status, message='An unknown error has occured.'):
        return render_template('pages/errors.html', error_code=status, message=message), status

    @app.errorhandler(401)
    def error_unauthorized(e):
        return show_error(401, 'Unauthorized')

    @app.errorhandler(403)
    def error_forbidden(e):
        return show_error(403, 'Forbidden')

    @app.errorhandler(404)
    def error_pagenotfound(e):
        return show_error(404, 'Page not found.')

    @app.errorhandler(500)
    def error_servererror(e):
        return show_error(500, 'An unknown error has occurred on the server.')
