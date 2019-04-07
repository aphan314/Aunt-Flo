from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time
import threading
from twilio.rest import Client
from keys import account_sid, auth_token, from_number, to_number


app = Flask(__name__)
current_time = None
change_count = 0

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


def _send_reminder():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body="PSA: Change your pad/tampon!!! Enter 'C' once you have changed it",
        to=to_number)
    print(message.sid)


def set_hour(message):
    timer = threading.Timer(int(message), _send_reminder())
    timer.start()
    return "Reminder set for " + str(message) + " *seconds*"

def set_emergency(message):
    return "x"

def set_change(message):

    return "Kudos! You changed your pad/tampon! Timer reset."

def set_period_over(message):
    return "okie yay!! u survived"



if __name__ == '__main__':
    app.run()
