# Python program to tell you if a screenplay passes the Bechdel test

import subprocess
import re

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

sample_lines = []
sample_lines.append(["Annie", "Hello, how are you? I am not talking about men"])
sample_lines.append(["Lauren", "Hey Annie, omg what are the odds I'm also not talking about Bob"])
sample_lines.append(["Annie", "No fucking way. We are so great"])
sample_lines.append(["Lauren", "Yeah ik right? This is awesome"])
sample_lines.append(["Melissa", "Hi I'm here to ruin ur perfect man-free convo"])
sample_lines.append(["Annie", "fuck"])

bechdel_test(sample_lines)

