from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

from random import randint
import datetime
import repeat
from keys import account_sid, auth_token, from_number, to_number, SENDGRID_KEY, image


app = Flask(__name__)

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
    response.message("\n\n" + reply)
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
        answer = "Oh no :( Aunt Flo will remind you to change your pad/tampon. Don't ovary react!!!" \
                 + "\n\nHow many *seconds* would you like to set the reminder for?"
    return answer


def _send_reminder():
    global timer
    del timer
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        body="PSA: Time to change your pad/tampon!!! " + "\n\n" +
                    "Enter 'C' once you have changed it or enter 'E' if your period has ended!",
        to=to_number)

def set_hour(message):
    global reminder
    reminder = int(message)
    global timer
    timer = repeat.RepeatingTimer(reminder, _send_reminder)
    timer.start()
    return "Okay sweetie :) \n\nReminder set for " + str(message) + " *seconds*"

def set_change():
    _set_count()
    global timer
    timer = repeat.RepeatingTimer(reminder, _send_reminder)
    timer.start()
    message = _get_message()
    return message + "\n\nTimer reset. See you in " + str(reminder) + " *seconds*!"

def _set_count():
    global count
    count += 1

def _get_message():
    messages = ["Great job! You changed your pad/tampon!",
                "Amazing! Thanks for practicing good hygeine!",
                "You're doing great sweetie! Your period will end!!",
                "Keep up the good work! Let's keep changing your pad/tampon!",
                "Yes! Goodbye bacterial infections and toxic shock syndrome!"]
    return messages[randint(0, len(messages))]


def set_period_over():
    global start_day
    global start_month
    now = datetime.datetime.now()
    _send_end_image()
    _send_email(start_day, start_month, now.day, now.month, count)

    return "\nWoo!! You survived another cycle :) \n\nYour cycle started on " \
            + str(start_month) + "/" + str(start_day) + " and ended on " + str(now.month) + "/" + str(now.day) \
            + ". You changed your pad/tampon " + str(count) + " times. \n\nSent the data to your email! \n<3 aunt flo"


def _send_end_image():
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_=from_number,
        media_url=image,
        to=to_number)


def _send_email(start_d, start_m, now_d, now_m, c):
    message = Mail(
        from_email='helloitsauntflo@gmail.com',
        to_emails='athenahacker2019@gmail.com',
        subject='Data About Your Cycle! <3',
        html_content='Hello sweetie!<br /> <br />Here is data about your cycle:<br /><br />' + 'Started on: ' + str(start_m)
                + '/' + str(start_d) + '<br />Ended on: ' + str(now_m) + '/' + str(now_d)
                + '<br />Number of times you changed your pad/tampon: ' + str(c) + '<br /><br />With Love, <br /> Aunt Flo'
                + '<br /><br /><i>AthenaHacks 2019</i>')
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)



if __name__ == '__main__':
    app.run()
