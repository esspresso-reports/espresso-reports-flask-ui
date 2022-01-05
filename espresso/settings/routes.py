from flask import Blueprint, session, current_app, render_template, request, redirect
from requests import get, post
import urllib.parse

from espresso.settings.util import convert_settings

bp = Blueprint('settings', __name__, template_folder="./templates")


@bp.route('/', methods=['GET'])
def show_settings():
    user_id = session['user_id']
    base_url = current_app.config['ESPRESSO_BACKEND_BASE_URL']

    hed = {'Authorization': 'Bearer ' + session.get('api_token')}
    user_settings = get(urllib.parse.urljoin(base_url, '/user/{user_id}/settings'.format(user_id=user_id)), headers=hed)

    return render_template("settings/settings.html", user_settings=user_settings.json())


@bp.route('/', methods=['POST'])
def save_settings():
    user_id = session['user_id']
    base_url = current_app.config['ESPRESSO_BACKEND_BASE_URL']

    hed = {'Authorization': 'Bearer ' + session.get('api_token')}

    new_settings = convert_settings(request.form)

    response = post(urllib.parse.urljoin(base_url, '/user/{user_id}/settings'.format(user_id=user_id)),
                    headers=hed, json=new_settings)

    if response.status_code != 200:
        return redirect('/settings', code=401)

    return redirect('/', code=302)
