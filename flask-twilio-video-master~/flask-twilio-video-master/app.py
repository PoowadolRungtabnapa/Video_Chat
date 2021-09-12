import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

load_dotenv()
twilio_account_sid = "ACb5da31851a81b91a1c7403da504d9f68"
twilio_api_key_sid = "SK9856450fd10b302f6852bc4a54674564"
twilio_api_key_secret = "m4JhQDOSDsunJMUMSCC5JRCYwXOBKNtu"
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

app = Flask(__name__)


def get_chatroom(name):
    for conversation in twilio_client.conversations.conversations.stream():
        if conversation.friendly_name == name:
            return conversation

    # a conversation with the given name does not exist ==> create a new one
    return twilio_client.conversations.conversations.create(
        friendly_name=name)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    print('1')
    print(request.get_json(force=True))
    print(request.get_json(force=True).get('username'))
    print(request.get_json(force=True).get('room'))
    username = request.get_json(force=True).get('username')
    
    room = request.get_json(force=True).get('room')
    if not username or not room :
        abort(401)
    conversation = get_chatroom(room)
    try:
        conversation.participants.create(identity=username)
        print(conversation.participants.create(identity=username))
    except TwilioRestException as exc:
        # do not error if the user is already in the conversation
        if exc.status != 409:
            raise

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room=room))
    token.add_grant(ChatGrant(service_sid=conversation.chat_service_sid))

    return {'token': token.to_jwt().decode(),
            'conversation_sid': conversation.sid}


if __name__ == '__main__':
    app.run(host='192.168.2.108')
