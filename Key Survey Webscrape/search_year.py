import os
import re
import csv
import codecs, chardet
# from multiprocessing import Pool
#
# pool = Pool()


# def process(path):
#     files = os.listdir(path)
#     # get half
#     if len(files) % 2 == 0:
#         r1 = pool.apply_async(chardet.detect(open(str(path+"{0}".format(files[range(len(files)/2)])), "rb").read()))
#         r2 = pool.apply_async(chardet.detect(open(str(path + "{0}".format(files[range(0, len(files)/2, len(files)/2)])), "rb")).read())
#         answer1 = r1.get(timeout=60)
#         answer2 = r2.get(timeout=60)
#         if answer1 is not None:
#             with open("format.txt", "w") as newFile:
#                 for key, value in answer1.items():
#                     newFile.write("{0}, {1}\n".format(key, value))
#                 newFile.close()
#         if answer2 is not None:
#             with open("format.txt", "w") as newFile:
#                 for key, value in answer1.items():
#                     newFile.write("{0}, {1}\n".format(key, value))
#                 newFile.close()
#     else:
#         get_all = pool.apply_async(chardet.detect(open(str(path + "{0}".format(files[range(len(files))])), "rb").read()))
#         one_blow = get_all.get(timeout=120)
#         if one_blow is not None:
#             with open("format.txt", "w") as newFile:
#                 for key, value in one_blow.items():
#                     newFile.write("{0}, {1}\n".format(key, value))
#                 newFile.close()
#
# process("C:\\Users\\User\\Downloads\\")
def search_csv():
    files = os.listdir(r'C:\\Users\\User\\Downloads\\')
    search = input("Please enter what you are searching for: ")
    for file in files:
        if '.csv' in file:
            with codecs.open(os.path.abspath(r'C:\Users\User\Downloads\{0}'.format(file)), "r", "utf8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if any(search in s for s in row):
                        print(file)
                        f.close()
                        break


def search_pdf():
    files = os.listdir(r'C:\\Users\\User\\Downloads\\')
    search = input("Please enter what you are searching for: ")
    for file in files:
        if '.pdf' in file and re.search(
                search, file):
            print(file)


search_pdf()