import os


def get_list():
    if os.path.isfile('names.txt'):
        with open('names.txt', 'r+') as file:
            text = file.read()
            splitedtext =text.split('\n')
            filtered = set(splitedtext)
            file.close()
        fileout = open('filterednames.txt', 'w')
        for item in filtered:
            fileout.write('%s/n' % item)
        fileout.close()

