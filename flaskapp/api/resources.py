from flaskapp import ma, db, guard
from flask_restful import Resource
from flask import request
from flaskapp.main.models import Message
from flaskapp.admin.models import User
from flask_praetorian import auth_required


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
        return {'messages': messages_schema.dump(messages)}, 200  # respond with the data and a 200 approved message

    @auth_required
    def delete(self):
        data = request.get_json(force=True)['message']
        message_id = data['id']
        message = Message.query.get(message_id)
        db.session.delete(message)
        db.session.commit()
        ret = {'status': True, 'response': f'Deleted message, id={message.id}'}
        return ret, 201

    @auth_required
    def put(self):
        data = request.get_json(force=True)['message']
        message_id = data['id']
        message = Message.query.get(message_id)
        if data['name'] != message.name:
            message.name = data['name']
        if data['body'] != message.body:
            message.body = data['body']
        if data['email'] != message.email:
            message.email = data['email']
        if data['phone'] != message.phone:
            message.phone = data['phone']
        db.session.commit()
        ret = {'status': True, 'response': f'Updated user {user.username}, id={user.id}'}
        return ret, 200

    @auth_required
    def post(self):
        data = request.get_json(force=True)['message']
        message = Message(name=data['name'], email=data['email'], body=data['body'], phone=data['phone'])
        db.session.add(message)
        db.session.commit()
        return ret, 201


class MessageAPI(Resource):
    # Defining get to get a message from the message model according to a id
    def get(self, message_id):
        message = Message.query.get_or_404(message_id) # returns 404 not found if it can't find the message.
        return message_schema.dump(message), 200


# Schemas
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    image_file = ma.auto_field()


users_schema = UserSchema(many=True)

class UsersAPI(Resource):
    
    def get(self):
        users = User.query.order_by(User.id.asc())
        return {'users': users_schema.dump(users)}, 200

    @auth_required
    def put(self):
        data = request.get_json(force=True)['user']
        user_id = data['id']
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User.query.get(user_id)
        if hashed_password != user.password:
            user.password = hashed_password
            user.api_password = guard.hash_password(hashed_password)
        if data['username'] != user.username:
            user.username = data['username']
        if data['email'] != user.email:
            user.email = data['email']
        db.session.commit()
        ret = {'status': True, 'response': f'Updated user {user.username}, id={user.id}'}
        return ret, 200

    @auth_required
    def post(self):
        data = request.get_json(force=True)['user']
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user = User(username=data['username'], email=data['email'], password=hashed_password, api_password=guard.hash_password(hashed_password))
        db.session.add(user)
        db.session.commit()
        ret = {'status': True, 'response': f'Added user {user.username}, id={user.id}'}
        return ret, 201

    @auth_required
    def delete(self):
        data = request.get_json(force=True)['user']
        user_id = data['id']
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'status': True, 'response': f'Deleted user {user.username}, id={user.id}'}, 200