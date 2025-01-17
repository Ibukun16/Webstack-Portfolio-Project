from models import storage_t
from app.api import app_views
from app.api.views.authe import basic_auth, token_auth


@app_views.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    storage_t.session.commit()
    return {'token': token}


@app_views.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke_token()
    storage_t.session.commit()
    return '', 204
