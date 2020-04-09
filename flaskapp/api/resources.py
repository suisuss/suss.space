from flaskapp import ma
from flask_restful import Resource
from flaskapp.main.models import Message


# Marshmallow MessageSchema
class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    body = ma.auto_field()
    date_submitted = ma.auto_field()


# Initaiting MessageSchema, one for all messages, the other for particular messages
messages_schema = MessageSchema(many=True)
message_schema = MessageSchema()


class MessagesAPI(Resource):
    # Defining get to get messages according to their 'id' in acending order
    def get(self):
        messages = Message.query.order_by(Message.id.asc())
        return messages_schema.dump(messages), 200  # respond with the data and a 200 approved message


class MessageAPI(Resource):
    # Defining get to get a message from the message model according to a id
    def get(self, message_id):
        message = Message.query.get_or_404(message_id) # returns 404 not found if it can't find the message.
        return message_schema.dump(message), 200
