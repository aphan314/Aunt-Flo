from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

import datetime
import repeat
from keys import account_sid, auth_token, from_number, to_number, SENDGRID_KEY, image


app = Flask(__name__)
current_time = None

global count
count = 0

global timer
timer = None

global reminder
reminder = 0

global start_day
start_day = 0

global start_month
start_month = 0


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
        answer = set_change()
    #ends app
    elif message == "e":
        answer = set_period_over()
    # first text
    else:
        now = datetime.datetime.now()
        global start_day
        start_day = now.day

        global start_month
        start_month = now.month
        answer = " \n Oh no :( Aunt Flo will remind you to change your pad/tampon. Don't ovary react!!! " \
                 + "How many *seconds* would you like to set the reminder for?"
    return answer


def _send_reminder():
    global timer
    del timer
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body="\nPSA: Time to change your pad/tampon!!! Enter 'C' once you have changed it or enter 'E' if your period is over!",
        to=to_number)

def set_hour(message):
    global reminder
    reminder = int(message)
    global timer
    timer = repeat.RepeatingTimer(reminder, _send_reminder)
    timer.start()
    return "\nOkay sweetie :) Reminder set for " + str(message) + " *seconds*"

def set_change():
    _set_count()
    global timer
    timer = repeat.RepeatingTimer(reminder, _send_reminder)
    timer.start()
    return "\nGreat job! You changed your pad/tampon! Timer reset. See you in " + str(reminder) + " *seconds*!"

def _set_count():
    global count
    count += 1


def set_period_over():
    send_end_image()
    now = datetime.datetime.now()
    global start_day
    global start_month
    return "\nWoo!! You survived another cycle :) Your cycle on " \
            + str(start_month) + "/" + str(start_day) + " and ended on " + str(now.month) + "/" + str(now.day) \
            + ". You changed your pad/tampon " + str(count) + " times. <3 aunt flo"


def send_end_image():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        media_url=image,
        to=to_number)


if __name__ == '__main__':
    app.run()
