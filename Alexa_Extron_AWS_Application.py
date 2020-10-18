
from __future__ import print_function
import socket
import logging
import json
import sys

    
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

def extronSend(myCommand):
    s = socket.socket()
    host = '62.103.65.43'            # Web or IP address of the Extron Control Processor (in String Format)
    port = 4001                  # port to listen on (as an Integer)
    s.connect((host, port))
    s.send(myCommand)
    s.close()
    '''s = socket.socket()
    host = '62.103.65.43'            # Web or IP address of the Extron Control Processor (in String Format)
    port = 5000                   # port to listen on (as an Integer)
    s.connect((host, port))
    s.send(myCommand)
    #extronResponse = (s.recv(1024)).decode("utf-8")    
    s.close()'''


# --------------- Functions that control the skill's behavior ------------------
def get_AudioCall_response(intent):
    session_attributes = {}
    card_title = "AudioCall"
    print(intent)
    speech_output = "You called " +intent['slots']['number']['value']
    extronSend(bytes("AudioCall: "+intent['slots']['number']['value'],'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




def get_inputOutputIntent_response(intent):    
    session_attributes = {}
    card_title = "inputOutputIntent"
    
    speech_output = " You send {0} to {1} ".format(intent['slots']['input']['value'],intent['slots']['output']['value'])
    extronSend(bytes("Matrix: "+intent['slots']['input']['value']+" "+intent['slots']['output']['value'], 'utf-8'))
    
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_lightsIntent_response(intent):    
    session_attributes = {}
    card_title = "lightsIntent"
    print(intent['slots']['lightsmode']['value'])
    speech_output = "You set lights {0}" .format(intent['slots']['lightsmode']['value'])
    extronSend(bytes("Lights: " + intent['slots']['lightsmode']['value'], 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_shadesIntent_response(intent):    
    session_attributes = {}
    card_title = "shadesIntent"
    print(intent)
    speech_output = "You set shades {0}" .format(intent['slots']['mode']['value'])
    extronSend(bytes("Shades: " + intent['slots']['mode']['value'], 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_volumeIntent_response(intent):    
    session_attributes = {}
    card_title = "volumeIntent"
    speech_output = "Volume command received"
    #print(intent)
    extronSend(bytes("Volume: " + intent['slots']['volumemode']['value'], 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_InputPresetIntent_response(intent):    
    session_attributes = {}
    card_title = "InputPresetIntent"
    speech_output = "You selected " + intent['slots']['Input']['value']
    extronSend(bytes("Preset: "+ intent['slots']['Input']['value'], 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))        

def get_monitorsIntent_response(intent):    
    session_attributes = {}
    card_title = "monitorsIntent"
    speech_output = "You set monitors " + intent['slots']['monitors_states']['value']
    extronSend(bytes("Monitors " + intent['slots']['monitors_states']['value'], 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_test_response():    
    session_attributes = {}
    card_title = "Test"
    speech_output = "This is a test message for debugging"
    extronSend(bytes("test", 'utf-8'))
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def get_bossIntent_response():    
    session_attributes = {}
    card_title = "BossIntent"
    speech_output = "You are the Boss Dimitris"
    reprompt_text = " "
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here    """    
    extronSend('Welcome'.encode())
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the extron control System!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = " "
    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample." \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts.
        One possible use of this function is to initialize specific 
        variables from a previous state stored in an external database
    """
    # Add additional code here as needed
    pass

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    # Dispatch to your skill's launch message
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "test":
        return get_test_response()
    elif intent_name=="inputoutputIntent":
        return get_inputOutputIntent_response(intent)
    elif intent_name=="lightsIntent":
        return get_lightsIntent_response(intent)
    elif intent_name=="shadesIntent":
        return get_shadesIntent_response(intent)
    elif intent_name=="volumeIntent":
        return get_volumeIntent_response(intent)
    elif intent_name=="InputPresetIntent":
        return get_InputPresetIntent_response(intent)
    elif intent_name=="monitorsIntent":
        return get_monitorsIntent_response(intent)
    elif intent_name=="bossIntent":
        return get_bossIntent_response()
    elif intent_name=="AudioCall":
        return get_AudioCall_response(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Incoming request...")

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])