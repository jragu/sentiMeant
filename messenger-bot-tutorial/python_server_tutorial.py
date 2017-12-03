## Beginning of logic

#importing watson

from watson_developer_cloud import ToneAnalyzerV3

# Importing operator for max value at what indexs

import operator

# Analyzes the message and returns emotions

def analyze_tone(message):
    tone_analyzer = ToneAnalyzerV3(
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',
        password='lJA5jjWG02iC',
        version='2016-05-19'
    )

    tone = tone_analyzer.tone(message, tones='emotion, language, social', sentences='true',content_type='text/plain')

    return parse_tone(tone)

def parse_tone(tone):
    eTones = ['disgust', 'fear', 'joy', 'sadness', 'anger']
    eVals = [0, 0, 0, 0, 0]
    lTones = ['analytical', 'confident', 'tentative']
    lVals = [0, 0, 0]
    sTones = ['openness_big5', 'conscientiousness_big5', 'extraversion_big5', 'agreeableness_big5',
              'emotional_range_big5']
    sVals = [0, 0, 0, 0, 0]

    # return array
    #rArr = []

    # ok so now to parse our json copying example here

    for i in tone['document_tone']['tone_categories']:
        for j in i['tones']:

            # process emotions
            if i['category_name'] == 'Emotion Tone':
                # print(j['tone_id'],"    ",j['score'])
                for index, feel in enumerate(eTones, 0):
                    if j['tone_id'] == feel:
                        eVals[index] = j['score']

            # process language
            if i['category_name'] == 'Language Tone':
                # print(j['tone_id'],"    ",j['score'])
                for index, feel in enumerate(lTones, 0):
                    if j['tone_id'] == feel:
                        lVals[index] = j['score']

            # process social
            if i['category_name'] == 'Social Tone':
                # print(j['tone_name'],"    ",j['score'])
                for index, feel in enumerate(sTones, 0):
                    if j['tone_id'] == feel:
                        sVals[index] = j['score']

    ##find_max_social(sVals,sTones)

    return find_max_emotion(eVals, eTones, lVals, lTones)

def find_max_emotion(eVals, eTones, lVals, lTones):
    index1, value= max(enumerate(eVals), key=operator.itemgetter(1))
    index2, value = max(enumerate(lVals), key=operator.itemgetter(1))
    return find_emoji(eTones[index1], lTones[index2])
    #mainEmotionValue=eTones[index]

def find_emoji(mainEmotionValue, mainLanguageValue):
    aDisgust = u'\U0001F61F'  # done
    cDisgust = u'\U0001F92E'  # done
    tDisgust = u'\U0001F922'  # done
    aFear = u'\U0001F626'  # done
    cFear = u'\U0001F631'  # done
    tFear = u'\U0001F630'  # done
    aJoy = u'\U0001F60F'  # done
    cJoy = u'\U0001F929'  # done
    tJoy = u'\U0001F642'  # done
    aSadness = u'\U0001F614'  # done
    cSadness = u'\U00002639'  # done
    tSadness = u'\U0001F641'  # done
    aAnger = u'\U0001F615'  # done
    cAnger = u'\U0001F92C'  # done
    tAnger = u'\U0001F604'  # done

    if mainEmotionValue=='disgust' and mainLanguageValue=='analytical':
       return(aDisgust)
    elif (mainEmotionValue=='disgust') and (mainLanguageValue=='confident'):
        return(cDisgust)
    elif (mainEmotionValue=='disgust') and (mainLanguageValue=='tentative'):
        return(tDisgust)
    elif mainEmotionValue=='fear' and mainLanguageValue=='analytical':
       return(aFear)
    elif (mainEmotionValue=='fear') and (mainLanguageValue=='confident'):
        return(cFear)
    elif (mainEmotionValue=='fear') and (mainLanguageValue=='tentative'):
        return(tFear)
    elif mainEmotionValue=='joy' and mainLanguageValue=='analytical':
       return(aJoy)
    elif (mainEmotionValue=='joy') and (mainLanguageValue=='confident'):
        return(cJoy)
    elif (mainEmotionValue=='joy') and (mainLanguageValue=='tentative'):
        return(tJoy)
    elif mainEmotionValue=='sadness' and mainLanguageValue=='analytical':
       return(aSadness)
    elif mainEmotionValue=='sadness' and mainLanguageValue=='confident':
        return(cSadness)
    elif (mainEmotionValue=='sadness') and (mainLanguageValue=='tentative'):
        return(tSadness)
    elif mainEmotionValue=='Anger' and mainLanguageValue=='analytical':
       return(aAnger)
    elif (mainEmotionValue=='Anger') and (mainLanguageValue=='confident'):
        return(cAnger)
    elif (mainEmotionValue=='Anger') and (mainLanguageValue=='tentative'):
        return(tAnger)


# Import Flask and request module from Flask
from flask import Flask, request

# Import request
import requests

# Importing JSON to test parse method

import json
# create a Flask app instance
app = Flask(__name__)

# Tokens from the Facebook page web hooks
ACCESS_TOKEN = "EAACyXvTVM0UBACJemZBZAL8f0ZBxm0JEEqPyWMoXqYgyYg9Gqnfsa9eZAAHEDd94eZAsnBoA9tWAZAr0TPB9wMSfwvgpfyiQa0GPoeLMobonzPMhNK3NqDPYzkrH0WN1Mh8rDuTt8aZAuR12H2XmIPzZCyXcRxk0MAVZCZCmqsDELxUQZDZD"
VERIFY_TOKEN = "secret"

# method to reply to a message from the sender
def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    # Post request using the Facebook Graph API v2.6
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)

# GET request to handle the verification of tokens
@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"

# POST request to handle in coming messages then call reply()
@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    pmessage = analyze_tone(message)
    reply(sender, pmessage)
    reply(sender, "Your text: \"" + message + "\" conveys the above emotional and language expression. "
                                              "Copy and paste the following expression to convey your "
                                              "message more accurately to your recipient: \""
           + message + " " + pmessage + ".\"")

    return "ok"

# Run the application.
if __name__ == '__main__':
    app.run(debug=True)
