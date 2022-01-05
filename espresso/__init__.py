import secrets

from flask import Flask, redirect, session

from espresso.config import config_by_name
from espresso.extensions import bs, oauth

from espresso.auth.routes import bp as auth_blueprint
from espresso.report.routes import bp as report_blueprint
from espresso.settings.routes import bp as settings_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    secret = secrets.token_urlsafe(32)
    app.secret_key = secret

    # initialize plugins
    bs.init_app(app)
    oauth.init_app(app)

    oauth.register(
        name='espresso',
        client_id='espresso',
        client_secret='3d087edb-3fa1-4df8-b6ed-579b13cfcdcf',
        access_token_url='http://localhost:8080/auth/realms/EspressoReports/protocol/openid-connect/token',
        access_token_params=None,
        authorize_url='http://localhost:8080/auth/realms/EspressoReports/protocol/openid-connect/auth',
        authorize_params=None,
        api_base_url='http://localhost:5001',
        client_kwargs={'scope': 'openid profile reports'},
        userinfo_endpoint='http://localhost:8080/auth/realms/EspressoReports/protocol/openid-connect/userinfo'
    )

    with app.app_context():
        # Register Blueprints
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(report_blueprint, url_prefix='/report')
        app.register_blueprint(settings_blueprint, url_prefix='/settings')

        @app.route('/')
        def index():
            api_token = session.get('api_token')

            if not api_token:
                # if not logged in redirect to login
                return redirect("/auth/login", code=302)
            else:
                # otherwise show the list of recent reports
                return redirect("/report")

    return app
