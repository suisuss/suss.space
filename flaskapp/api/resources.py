from flaskapp import ma, db, guard, bcrypt
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
        messages = Message.query.order_by(Message.id.asc()) # dumping the message according to the message_schema
        ret = ({'messages': messages_schema.dump(messages)}, 200) # respond with the data and a 200 approved message
        return ret[0], ret[1]


    def post(self):
        if data := request.get_json(force=True).get('message'):
            try:
                validated_data = message_schema.load(data)
                message = Message(name=validated_data['name'], email=validated_data['email'], body=validated_data['body'], phone=validated_data['phone'])
                db.session.add(message)
                db.session.commit()
                ret = ({'status': True, 'response': f'Created message, id={message.id}'}, 201)
            except:
                ret = ({'status': False, 'response': f'Unable to load a complete message'}, 400)
        else:
            ret = ({'status': False, 'response': f'No "message"'}, 400)
        return ret[0], ret[1]
    

    def put(self):
        if data := request.get_json(force=True).get('message'):
            try:
                validated_data = message_schema.load(data)
                message_id = validated_data['id']
                # Defining and checking that a valid id was passed
                if message := Message.query.filter_by(id=message_id).first():
                    message.name = validated_data['name']
                    message.body = validated_data['body']
                    message.email = validated_data['email']
                    message.phone = validated_data['phone']
                    db.session.commit()
                    ret = ({'status': True, 'response': f'Updated message, id={message.id}'}, 201)
                else:
                    ret = ({'status': False, 'response': f'Invalid message id'}, 400)

            except:
                ret = ({'status': False, 'response': f'Unable to load a complete message. "message" must include "id", "name", "body", "email" and "phone"'}, 400)
        else:
            ret = ({'status': False, 'response': f'No "message"'}, 400)
        return ret[0], ret[1]


    def delete(self):
        if data := request.get_json(force=True).get('message'):
            if message_id := data.get('id'):
                if message := Message.query.filter_by(id=message_id).first():
                    db.session.delete(message)
                    db.session.commit()
                    ret = ({'status': True, 'response': f'Deleted message, id={message.id}'}, 201)
                else:
                    ret = ({'status': False, 'response': f'Invalid message id'}, 400)
            else:
                ret = ({'status': False, 'response': f'No "id"'}, 400)
        else:
            ret = ({'status': False, 'response': f'No "message"'}, 400)

        return ret[0], ret[1]


class MessageAPI(Resource):
    # Defining get to get a message from the message model according to a id
    def get(self, message_id):
        message = Message.query.get_or_400(message_id) # returns 400 not found if it can't find the message.
        return message_schema.dump(message), 200


# Schemas
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    email = ma.auto_field()
    image_file = ma.auto_field()


users_schema = UserSchema(many=True, only=("username", "password", "email"))
user_schema0 = UserSchema(only=("username", "password", "email", "id")) # For PUT
user_schema1 = UserSchema(only=("username", "password", "email"))

class UsersAPI(Resource):
    
    def get(self):
        users = User.query.order_by(User.id.asc())
        return {'users': users_schema.dump(users)}, 200

    @auth_required
    def put(self):
        if data := request.get_json(force=True).get('user'):
            try:
                validated_data = user_schema0.load(data)
                user_id = validated_data['id']
                if user := User.query.filter_by(id=user_id).first():
                    hashed_password = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
                    user.password = hashed_password
                    user.api_password = guard.hash_password(hashed_password)
                    user.username = data['username']
                    user.email = data['email']
                    db.session.commit()
                    ret = ({'status': True, 'response': f'Updated user {user.username}, id={user.id}'}, 201)
                else:
                    ret = ({'status': False, 'response': f'User does not exist. Invalid "id"'}, 400)
            except:
                ret = ({'status': False, 'response': f'Unable to load a complete message. "message" must include "id", "username", "password", and "email"'}, 400)
        else:
            ret = ({'status': False, 'response': f'No "user" passed'}, 400)
        return ret[0], ret[1]

    @auth_required
    def post(self):
        if data := request.get_json(force=True).get('user'):
            try:
                validated_data = user_schema1.load(data)
                hashed_password = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
                user = User(username=validated_data['username'], email=validated_data['email'], password=hashed_password, api_password=guard.hash_password(hashed_password))
                db.session.add(user)
                db.session.commit()
                ret = ({'status': True, 'response': f'Added user {user.username}, id={user.id}'}, 201)
            except:
                ret = ({'status': False, 'response': f'"user" incomplete, must include "username", "password" and "email"'}, 400)
        else:
            ret = ({'status': False, 'response': f'No "user" passed'}, 400)
        return ret[0], ret[1]

    @auth_required
    def delete(self):
        if data := request.get_json(force=True).get('user'):
            if user_id := data.get('id'):
                if user := User.query.filter_by(id=user_id).first():
                    db.session.delete(user)
                    db.session.commit()
                    ret = ({'status': True, 'response': f'Deleted user, id={user.id}'}, 201)
                else:
                    ret = ({'status': False, 'response': f'Invalid user id'}, 400)
            else:
                ret = ({'status': False, 'response': f'"user" has no "id"'}, 400)
        else:
            ret = ({'status': False, 'response': f'"user" not supplied'}, 400)

        return ret[0], ret[1]

