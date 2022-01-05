from datetime import datetime, date, timedelta

import urllib.parse
from flask import Blueprint, render_template, session, request, current_app, url_for, redirect
from libgravatar import Gravatar
from requests import get, post

from espresso.report.service import is_report_outstanding

bp = Blueprint('reports', __name__, template_folder="./templates")


@bp.route('/')
def list_reports():
    user_id = session['user_id']
    user_mail = session['user_mail']
    user_name = session['user_name']
    base_url = current_app.config['ESPRESSO_BACKEND_BASE_URL']

    hed = {'Authorization': 'Bearer ' + session.get('api_token')}
    report_list = get(urllib.parse.urljoin(base_url, '/report'), params={'user_id': user_id}, headers=hed)

    return render_template("report/list_reports.html",
                           reports=report_list.json(),
                           current_user={'avatar': Gravatar(user_mail).get_image(),
                                         'username': user_name},
                           is_report_outstanding=is_report_outstanding(user_id))


@bp.route('/create', methods=('GET', 'POST'))
def create_report():
    base_url = current_app.config['ESPRESSO_BACKEND_BASE_URL']
    user_id = session['user_id']
    hed = {'Authorization': 'Bearer ' + session.get('api_token')}

    if request.method == 'POST':
        new_report = request.form.to_dict()
        new_report['user_id'] = user_id
        response = post(urllib.parse.urljoin(base_url, '/report'), json=new_report,
                        headers=hed)

        if response.status_code == 200:
            return redirect(url_for('reports.list_reports'))
        else:
            return render_template("report/report_formular.html")

    else:
        checkin = datetime.now().strftime("%H:%M")
        next_working_day = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        return render_template("report/report_formular.html", checkin=checkin, next_working_day=next_working_day)
