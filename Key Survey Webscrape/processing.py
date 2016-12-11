import os
import re
from collections import Counter
def get_list():
    if os.path.isfile('names.txt'):
        with open('names.txt', 'r+') as file:
            text = file.read()
            splitedtext =text.split('\n')
            filtered = set(splitedtext)
            file.close()
        fileout = open('filterednames.txt', 'w')
        for item in filtered:
            fileout.write('%s\n' % item)
        fileout.close()


def get_unique_surveys():
    if os.path.isfile('filterednames.txt'):
        # processing file to get the unique survey numbers
        with open('filterednames.txt', 'r+') as file:
            text = file.read()
            surveylist = []
            surveydictionary = {}
            surveyno = re.findall('survey:\d\d\d\d\d\d', text)
            surveylist.append(surveyno)

            get_unique = set(surveyno)
            for each in get_unique:
                surveydictionary[each] = surveyno.count(each)
                # write out results with key value pairs representing the survey and how many times it shows up in the list
        file.close()
        fileout = open('surveys.txt', 'w')
        for k, v in surveydictionary.items():
            fileout.write('{0} number:{1}\n'.format(k, v))
        fileout.close()

 #get_list()
get_unique_surveys()