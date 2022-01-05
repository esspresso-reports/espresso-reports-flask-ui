import urllib
from datetime import datetime

from flask import current_app, session
from requests import get


def is_report_outstanding(user_id):
    hed = {'Authorization': 'Bearer ' + session.get('api_token')}
    response = get(urllib.parse.urljoin(current_app.config['ESPRESSO_BACKEND_BASE_URL'], '/report/latest'),
                   params={'user_id': user_id},
                   headers=hed)

    if response.status_code == 200:
        report = response.json()

        check_in = datetime.strptime(report['check_in'], '%Y-%m-%dT%H:%M:%S.%f').date()
        next_working_day = datetime.strptime(report['next_working_day'], '%Y-%m-%d').date()
        today = datetime.now().date()

        return (today - check_in).days > 0 and (today - next_working_day).days >= 0
    return True
