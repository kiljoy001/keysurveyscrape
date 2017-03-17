import os
import re
import csv
import codecs, glob


def search_csv(search):
    files = os.listdir(r'C:\\Users\\User\\Downloads\\')
    for file in files:
        if '.csv' in file:
            with codecs.open(os.path.abspath(r'C:\Users\User\Downloads\{0}'.format(file)), "r", "utf8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if any(search in s for s in row):
                        print(file)
                        f.close()
                        break


def search_pdf(search):
    files = os.listdir(r'C:\\Users\\User\\Downloads\\')
    for file in files:
        if '.pdf' in file and re.search(
                search, file):
            print(file)


def process_list():
    files = glob.glob(r'C:\\Users\\User\\Downloads\\*.pdf')
    with open("listed_files.txt", "r") as listed:
        memList = listed.read().split("\n")
        report_dict = {}
        for each in memList:
            if re.search('\d+_\d+', each):
                if re.search('\d\d\d\d\d\d_\d\d\d\d\d\d', each):
                    report_dict[each[:13]] = each[14:]
                elif re.search('-1_\d+', each):
                    try:
                        report_dict[each[:9]] = each[10:]
                    except:
                        print("something wrong here")
                else:
                    print(each)
            else:
                print(each)
        listed.close()
        count = 0
        for key, value in report_dict.items():
            pattern = re.compile("\d\d\d\d\d\d_\d\d\d\d\d\d")
            if pattern.match(key):
                count += 1
        print(count)
        # for other in files:
        #     other = os.path.basename(other)
        #     if '.pdf' in other:
        #         if other[7:-4] in report_dict:
        #             print("True!")
        #         else:
        #             print("False! {0}".format(other))

process_list()