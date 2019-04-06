from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


@app.route('/sms', methods=['POST'])
def hello_world():
    resp = MessagingResponse()
    resp.message("Oh no :( How many hours until I remind you to change your pad/tampon?")
    return str(resp)


if __name__ == '__main__':
    app.run()
