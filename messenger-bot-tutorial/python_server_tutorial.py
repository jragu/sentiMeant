# Import Flask and request module from Flask
from flask import Flask, request

# Import request
import requests

# create a Flask app instance
app = Flask(__name__)

# Tokens from the Facebook page web hooks
ACCESS_TOKEN = "EAACyXvTVM0UBAAGkPknoRZCMYvrj2r3UJ2ed7XdLWrj4eNLy4XVoSdqsKg3bZCKRd2kANMJpNj7WsyGLMyE7glyZBBj6YQkEqPpq57S3NsK7noJT8IuZAx6MJnyUdJtaqRptHWT4fl55JuYroQjNjRm1MGJTAXiM1r14nYzEIgZDZD"
VERIFY_TOKEN = "secret"

# method to reply to a message from the sender
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    # Post request using the Facebook Graph API v2.6
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

# GET request to handle the verification of tokens
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"

# POST request to handle in coming messages then call reply()
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text'] + u'\U0001F604'
    reply(sender, analyze_tone(message))

    return "ok"

# Run the application.
if __name__ == '__main__':
    app.run(debug=True)



## Beginning of logic

#importing watson

from watson_developer_cloud import ToneAnalyzerV3

# Analyzes the message and returns emotions

def analyze_tone(message):
    tone_analyzer = ToneAnalyzerV3(
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',
        password='lJA5jjWG02iC',
        version='2016-05-19'
    )

    tone = tone_analyzer.tone(message, tones='emotion, language, social', sentences='true',content_type='text/plain')

