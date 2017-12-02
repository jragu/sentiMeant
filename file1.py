import re

import json

from os.path import join, dirname

from watson_developer_cloud import ToneAnalyzerV3



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

        print(names[usedName], line)



        # call the api here
        print(analyze_tone(line))
        # log sentiment,
        




#author:momen
def analyze_tone(statement):

    tone = ''

    tone_analyzer = ToneAnalyzerV3(
    
        username='31eed5f3-58e0-4739-a633-fa9cdb652848',

        password='lJA5jjWG02iC',

        version='12-01-2017'

    )

    ## please fix the variable of the file being opened

    with open(join(dirname(__file__), 'tone.json')) as tone_json:

        tone = tone_analyzer.tone(json.load(tone_json)['text'], tones='emotion, language, social', sentences='true',

                              content_type='text/plain')

    ##this is JSON being returned

    return(json.dumps(tone, indent=2))