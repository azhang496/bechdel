# Python program to tell you if a screenplay passes the Bechdel test

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from datetime import datetime
import string
import subprocess
import re


def convert_pdf(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def find_names(in_string):
    # content = [line.rstrip('\n') for line in open(in_string)] # <-- for files NOT strings
    chars = set('$,!@#%^&*()?-.:')
    listy = []
    sub_listy = []
    script = ''
    count = 0
    scene_number = 0
    # for line in content:
    for line in in_string.splitlines():
        if line[:1] == '(' or line[:1] == '*' or line[:1] == '\n':  # ADD MORE HERE FOR FEWER STAGE DIRECTIONS!!!!!!!!!
            continue
        if line.isdigit() and int(line) != scene_number:
            scene_number = int(line)
            sub_listy.append(script)
            listy.append(sub_listy)
            sub_listy = []
            script = ''
            sub_listy.append(line)
        elif line.isupper() and not any((c in chars) for c in line):
            count += 1
            if count > 1:
                sub_listy.append(script)
                listy.append(sub_listy)
            sub_listy = []
            script = ''
            sub_listy.append(line)
        else:
            script = script + line.translate(string.maketrans('', ''), string.punctuation) + ' '
    return listy


# male keywords
man_cave = ["man", "men", "guy", "guys", "he", "him", "himself", "his", "boy", "boyfriend", "boys", "boyfriends",
            "gentlemen"]


def is_woman(name):
    result = subprocess.check_output(["./name-genders", "gender-get_gender", name]).split()
    if result[len(result) - 1] == "female'":
        return True
    return False


def is_man(name):
    result = subprocess.check_output(["./name-genders", "gender-get_gender", name]).split()
    if result[len(result) - 1] == "male'":
        return True
    return False


def man_proof(lines):
    for line in lines:
        line = re.findall(r"[\w']+", line.lower())
        for word in line:
            # print word
            if word in man_cave:
                # print word
                # print "male keyword detected"
                return False
            if is_man(word):
                # print word
                # print "male name detected"
                return False
    return True


def bechdel_test(lines):
    women_count = 0
    women_lines = []
    for i in range(0, len(lines)):
        line = lines[i]
        if line[0].isdigit():
            # new scene, so reset conversation
            women_count = 0
            if women_lines:
                if man_proof(women_lines):
                    print women_lines
                    return "ur movie passes all 3 Bechdel tests! good job"
                del women_lines[:]
        if is_woman(line[0]) or 'LADY' in line[0] or 'DIDO' in line[0]:
            # print line[0]
            women_count += 1
            if women_count == 3:
                for j in range(i - 2, i + 1):
                    women_lines.append(lines[j][1])
                    # print women_lines
            if women_count > 3:
                women_lines.append(line[1])
        else:
            women_count = 0
            if women_lines:
                if man_proof(women_lines):
                    print women_lines
                    return "ur movie passes all 3 Bechdel tests! good job"
                del women_lines[:]
    return "weak. ur movie is probably sexist"


# ######################### TESTING WITH PDF #########################

startTime = datetime.now()
with open('trial.txt', 'w') as out_file:
    lst = find_names(convert_pdf('birdman.pdf'))
    print >> out_file, bechdel_test(lst)
print datetime.now() - startTime


# ######################### TESTING WITH TEXT FILE #########################
'''
lst = find_names('screenplay.txt')
with open('trial.txt', 'w') as out_file:
        print >> out_file, bechdel_test(lst)
'''