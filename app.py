from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms():
    message = request.form['Body']
    response = MessagingResponse()

    reply = formulate_reply(message)
    response.message(reply)
    return str(response)

def formulate_reply(message):
    message = message.lower().strip()
    answer = ""

    #user sends hour
    if message.isdigit():
        answer = set_hour(message)
    #changes timer
    elif message == "c":
        answer = set_change(message)
    #ends app
    elif message == "o":
        answer = set_period_over(message)
    # first text
    else:
        answer = "\n Oh no :( How many hours?"
    return answer

def set_hour(message):
    return "set_hour to 5. Reply x if you want to set an emergency"

def set_emergency(message):
    return "x"

def set_change(message):
    return "d"

def set_period_over(message):
    return "okie yay!! u survived"



if __name__ == '__main__':
    app.run()
