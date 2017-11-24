
import bson
import flask
import superdesk

from eve.utils import ParsedRequest
from superdesk.utc import utcnow
from superdesk.auth import TEMPLATE, RESOURCE
from superdesk.text_utils import get_text


def get_accepted_policy():
    user = get_session_user()
    return user and user.get('policy_accepted')


def normalize_policy(policy):
    """Ignore any formatting, get the list of words."""
    return get_text(policy, lf_on_block=True, space_on_elements=True).split()


def policy_compare(a, b):
    if not a or not b:
        return False
    return normalize_policy(a) == normalize_policy(b)


def get_session_user():
    if not flask.session.get('samlNameId'):
        return
    return superdesk.get_resource_service('users').find_one(req=None, email=flask.session['samlNameId'])


def init_app(app):
    app.add_template_global(get_accepted_policy)
    app.add_template_global(policy_compare)
    app.config['DOMAIN']['users']['schema'].update({
        'policy_accepted': {'type': 'string'},
        'policy_accepted_at': {'type': 'datetime'},
    })

    @app.route('/api/privacy_policy_accept', methods=['POST'])
    def privacy_policy_accept():
        user = get_session_user()
        if not user:
            flask.abort(403)
        sess = superdesk.get_resource_service(RESOURCE).find_one(req=None,
                                                                 _id=bson.ObjectId(flask.request.form['session']))
        if not sess:
            flask.abort(403)
        superdesk.get_resource_service('users').system_update(user['_id'], {
            'policy_accepted': flask.request.form['policy'],
            'policy_accepted_at': utcnow(),
        }, user)
        return flask.render_template(TEMPLATE, data=dict(
            type=RESOURCE,
            _id=str(sess['_id']),
            user=str(user['_id']),
            token=str(sess['token']),
        ))

    @app.route('/api/privacy_policy_status')
    def privacy_policy():
        user = get_session_user()
        if not user or user.get('user_type') != 'administrator':
            flask.abort(403)
        req = ParsedRequest()
        req.max_results = 200
        users = superdesk.get_resource_service('users').get(req, None)
        return flask.render_template('privacy_policy_users.html', users=users)
