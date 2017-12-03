## Filename: server.py

from flask import Flask, request

app = Flask(__name__)


import os

from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
   if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
   #      if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
   #          return "Verification token mismatch", 403
   #      return request.args["hub.challenge"], 200

    return "Hello world", 200

if __name__ == '__main__':
    app.run(host='52.40.198.72', port=8000)

import requests

import json
import re
##from watson_developer_cloud import ToneAnalyzerV3

from flask import Flask, stream_with_context, request, Response, url_for

import operator


app = Flask(__name__)

ACCESS_TOKEN = "EAAUwpnlCIIwBAJl6WEHQkMNRWFE2M9dgZC3acToPFVP3abpDWxfxowDV5oabAGfMrE94ozGe2JwGscM3wveATl1t0JKFJ4WqVgacEO2jTunvqxoSPtWKSQszPb1RY8cAHH5nTZCOIpj2TLsX1CSjbUwTHbT1auAk6wmsR8vQZDZD"





def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg + 'ADD ORIGINAL MESSAGE HERE'}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    parsedmessage = analyze_tone(message)
    reply(sender, parsedmessage)

    return "ok"

def analyze_tone(message):
    tone_analyzer = ToneAnalyzerV3(
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',
        password='lJA5jjWG02iC',
        version='2016-05-19'
    )

    tone = tone_analyzer.tone(message, tones='emotion, language, social', sentences='true',content_type='text/plain')

    ##this is JSON being returned

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
    rArr = []

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

    return find_emoji(find_max_emotion(eVals, eTones), find_max_language(lVals, lTones))




def find_max_emotion(eVals, eTones):
    index, value= max(enumerate(eVals), key=operator.itemgetter(1))
    global mainEmotionValue
    mainEmotionValue=eTones[index]

def find_max_language(lVals, lTones):
    index, value= max(enumerate(lVals), key=operator.itemgetter(1))
    mainLanguageValue=lTones[index]
    return mainLanguageValue

##def find_max_social(sVals, sTones):
   ## index, value= max(enumerate(sVals), key=operator.itemgetter(1))
  ##  mainSocialValue=sTones[index]


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


if __name__ == '__main__':
    app.run(debug=True)