from os import listdir
from os.path import isfile, join
import csv
import string
from nltk.corpus import stopwords


def save(filename, dictionary):
    w = csv.writer(open(filename, "w"))
    for key, val in dictionary.items():
        w.writerow([key, val])


def load(filename):
    d = {}
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        for rows in reader:
            if len(rows) == 2:
                d[rows[0]] = float(rows[1])
    return d


def cleaner(text):
    text = text.lower()
    translation_table = dict.fromkeys(map(ord, string.punctuation + '\0'), None)
    stopWords = set(stopwords.words('english'))
    stopWords.add("subject")
    text = text.replace('\n', ' ')
    text = text.translate(translation_table)
    mail = text.split(' ')
    mail = [word for word in mail if word not in stopWords]
    return mail

def train(filename):
    files = [f for f in listdir(filename) if isfile(join(filename, f))]
    dictionary = {}
    counter = 0
    for file in files:
        file = open(filename + "/" + file, errors="ignore")
        text = file.read()
        file.close()
        mail = cleaner(text)
        for word in mail:
            counter += 1
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    fileCount = len(files)
    for word in dictionary.keys():
        dictionary[word] = float(dictionary[word]) / fileCount
    dictionary["fileCount"] = fileCount
    return dictionary


def classify(input, diction, priori):
    input = cleaner(input)
    p = 1
    for word in input:
        if word in diction.keys():
            p *= diction[word]
        else:
            p *= 1/diction["fileCount"]+len(diction)+1
    p *= priori
    return p


def trainNsave():
    save("spam_train_results.csv", train("spam"))
    save("ham_train_results.csv", train("ham"))


def test():
    hamDict = load("ham_train_results.csv")
    spamDict = load("spam_train_results.csv")
    files = [f for f in listdir("input") if isfile(join("input", f))]
    spamC = hamC = 0
    for file in files:
        file = open("input" + "/" + file, errors = "ignore")
        text = file.read()
        file.close()
        ham = classify(text, hamDict, 0.67)
        spam = classify(text, spamDict, 0.33)
        if ham <= spam:
            spamC += 1
        else:
            hamC += 1
    print("Spam:\t" + str(hamC))
    print("Ham:\t" + str(spamC))


trainNsave()
test()
