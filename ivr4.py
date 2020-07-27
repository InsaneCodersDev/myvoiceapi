import requests
import time
import datetime
from flask import Flask,session
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
import pymongo
import dns
# from datetime import date


reject=False
blocking=False



client = pymongo.MongoClient("mongodb+srv://ovi:ovi@cluster0-ivsyl.mongodb.net/Attendnace?retryWrites=true&w=majority")
db = client.Attendnace
# userids=list()

employ_attendance = db.employ_attendance_logins
employ = db.employ_registrations





app= Flask(__name__)
app.secret_key="insanecoders"

@app.route('/')
@app.route('/ivr')
def Home():
    return render_template('index.html')


@app.route('/ivr/welcome', methods=['POST'])
def welcome():
    session["repeat"]=0
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
    option_actions = {'1': _getuserid,
                      '2': _forward_call}

    if selected_option in option_actions.keys():
        response = VoiceResponse()
        option_actions[selected_option](response)
        return twiml(response)

   
        
       
    return ""




def _getuserid(response):
    
    print("In userid function...\n")
    # response.say("Enter your User ID on Keypad")
    with response.gather(
        num_digits=4, action=url_for('record'), method="POST"
    ) as g:
        g.say(message="Enter your User ID on Keypad")



              
@app.route('/ivr/record', methods=['POST'])
def record():
    print("In record function.......")
    response = VoiceResponse()
    repeat=session["repeat"]
    if repeat == 0:
        userid = request.form['Digits']
        print(userid)
        userid=int(userid)
        print(userid)

    
        b = employ.find({'userid':userid})
        have_list = False if len(list(b)) else True
        if(have_list):
            response.say('You entered wrong userid.Try again')
            return _redirect_welcome(response)

        for i in employ.find({'userid':userid},{'username':1}):
            response.say("Welcome "+i['username'] + " Speak your passphrase after the beep sound. Then press any key to end the recording.")
            session["username"]=i["username"]
            session["repeat"]=1
            # print(userids[0])
            # time.sleep(2)
            
       
        # with response.gather(num_digits=1, action=url_for('process'), method="POST") as g:
        #     g.say(message="Press Hash to continue")
            
        # response.say("Press Hash to continue")
        
    response.record(timeout=0,transcribe=False,playBeep=True,maxLength=5,action=url_for('process'))
    return twiml(response)


@app.route('/ivr/process', methods=['POST'])
def process():
    print("In process function")
    global userids
    username=session["username"]
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
        if identity==username:
            response.say("Welcome "+ str(identity))
            today = datetime.date.today()
            date = int(today.strftime("%d"))
            month = int(today.strftime("%m"))
            year = int(today.strftime("%Y"))
            now = datetime.datetime.now()
            # dd/mm/YY H:M:S
            hr = int(now.strftime("%H")) + 5
            min = int(now.strftime("%M")) + 30
            if(min >= 60):
                hr = hr + 1
                min = min - 60
            if(hr>=24):
                date = date + 1
                hr = hr - 24
            time = str(hr) + ':' + str(min)
            atd = employ_attendance.find({'username':username,'date':date})
            count = False if len(list(atd)) else True
            if(count):
                employ_attendance.insert_one({'username':username,'date':date,'month':month,'year':year,'time':time,'interface':'Landline','attendance':True})
                response.say("Your Attendance is marked.")
            else:
                response.say('Your Attendance already marked')
            response.hangup()
        else:
            response.say('Not Recognized. Try Again.')
            return _redirect_record(response)
        return twiml(response)
    else:
        print("Not Recognized....")
        response.say("Not recognised.Try Again.")    
        return _redirect_record(response)


    return response






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


def _redirect_record(response):
    print("Redirecting to record....\n") 
    #response = VoiceResponse()
    response.say("Speak your passphrase after the beep sound. Then press any key to end the recording. ")
    response.redirect(url_for('record'))

    return twiml(response)

if __name__ == "__main__":
    app.run(debug=True, port=8000, host="0.0.0.0")
