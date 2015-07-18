# Python program to tell you if a screenplay passes the Bechdel test

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
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
 #   content = [line.rstrip('\n') for line in open(filename)] <-- if files were func input
    listy = []
    sub_listy = []
    script = ''
    count = 0
    for line in in_string.splitlines():
        if line.isupper() and line.isalpha():
            if count > 0:
                sub_listy.append(script)
                listy.append(sub_listy)
            sub_listy = []
            script = ''
            sub_listy.append(line)
            count += 1
        else:
            script = script + line.translate(string.maketrans('',''), string.punctuation) + ' '
    return listy


# male keywords
man_cave = ["man", "men", "guy", "guys", "he", "him", "his"]

def isWoman(name):
    result = subprocess.check_output(["./name-genders", "gender-get_gender", name]).split()
    if result[len(result) - 1] == "male'":
        return False
    return True

def man_proof(lines):
    for line in lines:
        line = re.findall(r"[\w']+", line.lower())
        for word in line:
            print word
            if word in man_cave:
                print "male keyword detected"
                return False
            if not isWoman(word):
                print "male name detected"
                return False
    return True

def bechdel_test(lines):
    women_count = 0
    women_lines = []
    not_sexist = False

    for i in range(0, len(lines)):
        line = lines[i]
        if isWoman(line[0]):
            women_count += 1
            if women_count == 3:
                not_sexist = True
                for j in range(i-2, i+1):
                    women_lines.append(lines[j][1])
            if women_count > 3:
                women_lines.append(line[1])

        else:
            women_count = 0
            if women_lines:
                if not man_proof(women_lines):
                    not_sexist = False
                    print "weak. ur movie only passed the first 2 Bechdel tests"
            del women_lines[:]

        print "women count: %d" % women_count
        print women_lines

    if women_lines:
        if not man_proof(women_lines):
            not_sexist = False

    if not_sexist:
        print "ur movie passes all 3 Bechdel tests! good job"
    else:
        print "weak. ur movie only passes 2 Bechdel tests"


######################### TESTING #########################

with open('test.txt', 'w') as out_file:
    print >> out_file, find_names(convert_pdf('birdman_mini_script_book.pdf'))

'''
print find_names('example.txt')

with open('test.txt', 'w') as out_file:
    print >> out_file, find_names('example.txt')
'''



sample_lines = []
sample_lines.append(["Annie", "Hello, how are you? I am not talking about men"])
sample_lines.append(["Lauren", "Hey Annie, omg what are the odds I'm also not talking about Bob"])
sample_lines.append(["Annie", "No fucking way. We are so great"])
sample_lines.append(["Lauren", "Yeah ik right? This is awesome"])
sample_lines.append(["Melissa", "Hi I'm here to ruin ur perfect man-free convo"])
sample_lines.append(["Annie", "fuck"])

bechdel_test(sample_lines)

