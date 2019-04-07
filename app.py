from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import time
import threading
from twilio.rest import Client
from keys import account_sid, auth_token


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

def gfg():
    print("gfg")
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_="+17148810022",
        body="Hello! Change your pad/tampon!",
        to="+14084665757")
    print(message.sid)


def set_hour(message):
    current_time = time.time()
    print(current_time)
    timer = threading.Timer(4.0, gfg)
    timer.start()
    return "Reminder set for " + str(message) + "(seconds)"

def set_emergency(message):
    return "x"

def set_change(message):
    change_time = time.time()
    print(change_time)
    return "You changed your pad/tampon!"

def set_period_over(message):
    return "okie yay!! u survived"



if __name__ == '__main__':
    app.run()
