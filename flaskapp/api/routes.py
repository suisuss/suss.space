from flask import Blueprint
from flaskapp.api.resources import MessagesAPI, MessageAPI

# Initiating API blueprint
api_bp = Blueprint('api', __name__)


# Intializing API routes function used when intializing the app
def initialise_api_routes(api):
    api.add_resource(MessagesAPI, '/api/messages')
    api.add_resource(MessageAPI, '/api/message/<int:message_id>')
