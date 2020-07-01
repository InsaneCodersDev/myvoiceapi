import requests
import time
import datetime
from flask import Flask
from recognize2 import recognize
from flask import (
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
)
from twilio.twiml.voice_response import VoiceResponse
from view_helpers import twiml

reject=False
blocking=False


app= Flask(__name__)

@app.route('/')
@app.route('/ivr')
def Home():
    return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    print("\nIn welcome function.....")
    # print(request.form)
    response = VoiceResponse()
    number=request.form['From']
    print(number)
    if number!="+919969149297" and blocking==True:
        # To not take calls from unknown numbers. 
        # Just can receive call from the landline number from office.
        if reject==True:
            response.reject(reason='rejected')  
        else:
            response.say(message="Your call is rejected. In order to access Voice your ID you need to call from office landlines only.")
            response.hangup()
    
    with response.gather(
        num_digits=1, action=url_for('menu'), method="POST"
    ) as g:
        g.say(message="Welcome to Voice your ID attendance marking system" +
              "Press 1 for Marking your attendance" +
              "Press 2 for Customer Care")
    return twiml(response)


@app.route('/ivr/menu', methods=['POST'])
def menu():
    print("\nIn Menu function.....")
    # print(request.form)

    selected_option = request.form['Digits']
    option_actions = {'1': _record,
                      '2': _forward_call}

    if selected_option in option_actions.keys():
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)

    elif selected_option=='#':

        response=VoiceResponse()
        filename=str(datetime.datetime.now())
        filename="_".join(filename.split())
        filename="_".join(filename.split("-"))
        filename="_".join(filename.split(":"))
        filename="_".join(filename.split("."))+".wav"
        url = request.form['RecordingUrl']
        print(url)
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        print(filename)
        identity=recognize(filename)
        if  identity!="Not identified":
            response.say("Welcome "+ str(identity))
            response.say("Your Attendance is marked.")
            response.hangup()
            return twiml(response)
        else:
            print("Not Recognized....")
            response.say("Not recognised.Try Again.")    
            return _redirect_welcome(response)

    return ""




def _record(response):
    print("In response fucntion...\n")
    response.say("Please speak the passphrase to mark your attendance after the beep sound. Then Press hash to stop recording.")
    response.record(timeout=0,finishOnKey="#",transcribe=False,playBeep=True)
    

def _forward_call(response):
    response.say("Forwarding Call to Customer Care.")
    response.dial("+919869417195")
    return twiml(response)


def _redirect_welcome(response):
    print("Redirecting....\n") 
    #response = VoiceResponse()
    response.say("Returning to the main menu")
    response.redirect(url_for('welcome'))

    return twiml(response)

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
