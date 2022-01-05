import urllib.parse

from flask import Blueprint, redirect, session, current_app
from requests import put

from espresso.extensions import oauth

bp = Blueprint('auth', __name__)


@bp.route('/login')
def login():
    return oauth.espresso.authorize_redirect("http://localhost:5001/auth/authorize")


@bp.route('/authorize')
def authenticate():
    base_url = current_app.config['ESPRESSO_BACKEND_BASE_URL']
    token = oauth.espresso.authorize_access_token()
    userinfo = oauth.espresso.userinfo()

    new_user = {
        'id': userinfo['sub'],
        'email': userinfo['email'],
        'email_verified': userinfo['email_verified'],
        'is_disabled': False,
        'settings': {}
    }

    put(urllib.parse.urljoin(base_url, '/user'), json=new_user)

    session['api_token'] = token['access_token']
    session['user_id'] = userinfo['sub']
    session['user_mail'] = userinfo['email']
    session['user_name'] = userinfo['preferred_username']

    return redirect('/', code=302)


@bp.route('/logout')
def logout():
    token = session.pop('api_token')
    session.pop('user_mail')
    session.pop('user_name')

    return redirect('http://localhost:8080/auth/realms/EspressoReports/protocol/openid-connect/logout?redirect_uri=http://localhost:5001/', code=302)
