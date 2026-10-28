import logging
import socket
import json
import sys

from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


def extronSend(myCommand):
    s = socket.socket()
    
    host = '192.168.100.198'            # Web or IP address of the Extron Control Processor (in String Format)
    port = 4000                  # port to listen on (as an Integer)
    s.connect((host, port))
    s.send(myCommand)
    extronResponse = (s.recv(1024)).decode("utf-8")
    s.
    s.close()
    return extronResponse.encode('utf-8')
extronSend(json.dumps(['startup', 'power', 'system', 'on', '', None]))

@ask.launch
def launch():
    speech_text = 'Welcome to the Extron Alexa Skill'
    return question(speech_text).reprompt(speech_text).simple_card('Extron Skill', speech_text)



@ask.intent('AMAZON.YesIntent')
def yesSend():
    speech_text = extronSend(json.dumps(['YesIntent', 'yes', '', '', '', None]))
    return statement(speech_text)

@ask.intent('AMAZON.NoIntent')
def noSend():
    speech_text = extronSend(json.dumps(['NoIntent', 'no', '', '', '', None]))
    return statement(speech_text)

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = extronSend(json.dumps(['HelpIntent', '', '', '', '', None]))
    return question(speech_text).reprompt(speech_text).simple_card('Help', speech_text)

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)
