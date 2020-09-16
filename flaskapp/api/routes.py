from flask import Blueprint, jsonify, request
from flaskapp.api.resources import MessagesAPI, MessageAPI, UsersAPI
from flaskapp import guard, app
from flaskapp.admin.models import User

# Initiating API blueprint
api_bp = Blueprint('api', __name__)


# Intializing API routes function used when intializing the app
def initialise_api_routes(api):
    api.add_resource(MessagesAPI, '/api/messages')
    api.add_resource(MessageAPI, '/api/message/<int:message_id>')
    api.add_resource(UsersAPI, '/api/users')


# Flask-Praetorian
@api_bp.route('/api/admin/login', methods=['POST'])
def api_admin_login():
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":test","password":"test"}'
    """
    req = request.get_json(force=True)

    username = req.get('username', None)
    password = req.get('password', None)

    user = guard.authenticate(username, password)
    access_token = guard.encode_jwt_token(user)

    user = User.query.filter_by(username=username).first()

    ret = {
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'image_file': user.image_file 
        }}

    return (jsonify(ret), 200)


@api_bp.route('/api/admin/refresh')
def api_admin_refresh():
    json_data = request.get_json()
    access_token = guard.refresh_jwt_token(json_data['token'])
    return jsonify({'access_token' : access_token})
    