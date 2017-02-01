import os
import re
import csv
import chardet

files= os.listdir(r'C:\Users\User\Downloads')
for file in files:
    if '.csv' in file:
        chardet.detect(open(os.path.abspath(r'C:\Users\User\Downloads\{0}'.format(file)), "rb"))
        # pattern = re.compile()
        #for i, line in chardet.detect(open(os.path.abspath(r'C:\Users\User\Downloads\{0}'.format(file)), newline='', encoding='cp1252')):
            # print(line)
