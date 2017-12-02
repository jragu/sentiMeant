import json
import re

from watson_developer_cloud import ToneAnalyzerV3


def analyze_tone(statement):
    tone_analyzer = ToneAnalyzerV3(
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',
        password='lJA5jjWG02iC',
        version='2016-05-19'
    )

    tone = tone_analyzer.tone(statement, tones='emotion, language, social', sentences='false',content_type='text/plain')

    ##this is JSON being returned

    return(tone)


#jr
def parse_tone(tone):
    eTones = ['disgust','fear','joy','sadness']
    eVals = [0,0,0,0]
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

        json_data = json.dumps(data)    

        return json_data


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
        print(makeItJsonY(sentiments, line, names[usedName]))

        #send to web browser

