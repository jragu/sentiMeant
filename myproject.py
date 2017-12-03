from flask import Flask, stream_with_context, request, Response, url_for, render_template

import json
import re

from watson_developer_cloud import ToneAnalyzerV3

application = Flask(__name__)

def analyze_tone(statement):
    tone_analyzer = ToneAnalyzerV3(
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',
        password='lJA5jjWG02iC',
        version='2016-05-19'
    )

    tone = tone_analyzer.tone(statement, tones='emotion, language, social', sentences='false',content_type='text/plain')

    ##this is JSON being returned

    return(tone)

#kristen and jordan
def processColor(value, emotion):

    if emotion == 'disgust':

        if value < .20:

            #color 1

            return #A6B49E

        if .2 <= value and value < .4:

            #color 2

            return #89A481

        if .4 <= value and value <.6:

            #col 3

            return #6B9463

        if .6 <= value and value < .8:

            return #4E8446

        if .8 <= value and value < 1:

            return #4E8446

    if emotion == 'fear':

        if value < .20:

            #return color 1

            return #B4ADB3

        if .2 <= value and value < .4:

            #color 2

            return #A597AB

        if .4 <= value and value <.6:

            #col 3

            return #9580A3

        if .6 <= value and value < .8:

            return #866A9B

        if .8 <= value and value < 1:

            return #775493

    if emotion == 'joy':

        if value < .20:

            #return color 1

            return #CFCFB2

        if .2 <= value and value < .4:

            #color 2

            return #DADBA8

        if .4 <= value and value <.6:

            #col 3

            return #E5E79F

        if .6 <= value and value < .8:

            return #F0F395

        if .8 <= value and value < 1:

            return #FBFF8C

    if emotion == 'sadness':

        if value < .20:

                    #return color 1
            return  #B7C2C4

        if .2 <= value and value < .4:
            #color 2

            return #ABC0CC

        if .4 <= value and value <.6:

            #col 3
            return #9FBED4

        if .6 <= value and value < .8:

            return #93BCDC

        if .8 <= value and value < 1:

            return #87BBE5

    if emotion == 'anger':

        if value < .20:

            #return color 1
            return  #CAA099

        if .2 <= value and value < .4:

            #color 2

            return #D17C77

        if .4 <= value and value <.6:

            #col 3

            return #D75854

        if .6 <= value and value < .8:

            return #DE3332

        if .8 <= value and value < 1:

            return #E51010


def parse_tone(tone):
    eTones = ['disgust','fear','joy','sadness','anger']
    eVals = [0,0,0,0,0]
    lTones = ['analytical','confident','tentative']
    lVals = [0,0,0]
    sTones = ['openness_big5', 'conscientiousness_big5', 'extraversion_big5', 'agreeableness_big5', 'emotional_range_big5']
    sVals = [0,0,0,0,0]

    #return array
    rArr = []

    #ok so now to parse our json copying example here

    for i in tone['document_tone']['tone_categories']:
        for j in i['tones']:
        
            #process emotions
            if i['category_name'] == 'Emotion Tone':
                #print(j['tone_id'],"    ",j['score'])
                for index, feel in enumerate(eTones, 0):
                    if j['tone_id'] == feel:
                        eVals[index] = j['score']

            #process language 
            if i['category_name'] == 'Language Tone':
                #print(j['tone_id'],"    ",j['score'])
                for index, feel in enumerate(lTones, 0):
                    if j['tone_id'] == feel:
                        lVals[index] = j['score']
        
            #process social
            if i['category_name'] == 'Social Tone':
                #print(j['tone_name'],"    ",j['score'])
                for index, feel in enumerate(sTones, 0):
                    if j['tone_id'] == feel:
                        sVals[index] = j['score']
    
    #add everything to the return array
    rArr.append(eTones)
    rArr.append(eVals)
    rArr.append(lTones)
    rArr.append(lVals)
    rArr.append(sTones)
    rArr.append(sVals)

    return rArr

def makeItJsonY(niceArray, text, name):
        #first turn to dictionaries
        emotions = dict(zip(niceArray[0],niceArray[1]))
        language = dict(zip(niceArray[2],niceArray[3]))
        sentiment = dict(zip(niceArray[4],niceArray[5]))

        #create json object
        data = {}
        data['emotions'] = emotions
        data['language'] = language
        data['sentiment'] = sentiment

        data['text'] = text

        data['name'] = name
    
        #add a json_dumps(data)
        return data

@application.route("/")
def hello():
    return render_template('index.html')


@application.route('/stream')
def streamed_response():
    def generate():

        myFile = open("silenceOfLambs.txt", "r")
        names = []
        sentiments = []
        noMatch = 0
        firstLine = 0
        index = 0
        usedName = 0

        for line in myFile:
            if firstLine == 0:
                line = line.strip('\n')
                noMatch = 0
                
                # Check to see if the name has been seen before
                for index, name in enumerate(names, 0):
                # matches name + any number of characters
                
                    if re.match( name +'*' ,line):
                        noMatch = 1
                        usedName = index
                
                if noMatch == 0:
                # didn't match so we'll add to list
                    names.append(line)
                    usedName = len(names ) -1
                firstLine = 1
            else:
                firstLine = 0
                # call the api here
                sentiments = parse_tone(analyze_tone(line))
                # and log sentiment,
                #now push to webbrowser

                #array, text, name
                json_data = makeItJsonY(sentiments, line, names[usedName])

                #let's find the largest valued emotion
                largestEmo = 'disgust'
                #largestSent = ""
                #largestLang = ""

                #find largest emotion
                for key in json_data['emotions']:
                    if json_data['emotions'][key] > json_data['emotions'][largestEmo]:
                        largestEmo = key
                
                
                """
                for key in json_data['language']:
                    if json_data['language'][key] > json_data['language'][largestLang]:
                        largestLang = key
                """


                """
                for key in json_data['sentiment']:
                    if json_data['sentiment'][key] > json_data['sentiment'][largestSent]:
                        largestSent = key
                """                    

                yield '<br>'
                yield '<br>'
                yield json_data['name']
                yield '<br>'
                yield '<div class="bubble1">'
                yield json_data['text']
                yield '</div>'
                yield '<br>'
                yield '<br>'
                yield str(json_data['emotions'][largestEmo])
    return Response(stream_with_context(generate()))

#@application.route('/fbPoint')
#add more later

if __name__ == "__main__":
    application.run(host='0.0.0.0')