"""
Created On: 20th Sept 2015
@author: Amitayush Thakur,Jaiwant Rawat,Ashish Tilokani
"""
import os
from DatabaseParser.models import WordTable, DocFreqTable, DocClass


FREQ_THRESHOLD_PERCENT = 0.3
STOP_WORD_LIST_FILENAME = 'DatabaseParser/stopwordsList.txt'
# Create your views here.
PATH_TO_DATASET = '../TrainingData/'
MAX_NUM_OF_WORDS_READ = 300

def onlyascii(char):
    if ord(char) < 48 or ord(char) > 127: return ''
    else: return char

def get_my_string(file_path):
    s = ""
    l = len(file_path)
    i = 0
    while i < l:
        s += onlyascii(file_path[i])
        i += 1
    s = s.lower()
    return s

def loadStopWords(filename):
    fp = open(filename,'r');
    words  = fp.read().split('\n');
    stopWordDict = {}
    for word in words:
        stopWordDict[word] = True
    return stopWordDict

def parseTextToDb(fileList):
    #load all stop words in main memory
    stopWordDict = loadStopWords(STOP_WORD_LIST_FILENAME)
    #logic for counting and reading the text file
    for file in fileList:
        fileToken = file.split('/')
        if len(DocClass.objects.filter(className = fileToken[1],docName=fileToken[2])) != 0:
            continue
        DocClass.objects.create(className = fileToken[1],docName=fileToken[2])
        fp = open(file,encoding="latin-1")
        print('Opening the file '+file+'..... \n\n')
        wordList = fp.read().split()
        cnt = 0
        print('Removing stop words:')
        for word in wordList:
            word = get_my_string(word)
            if word in stopWordDict.keys():
                print(word)
                continue
            if len(WordTable.objects.filter(word=word,docName = fileToken[2]))== 0 :
                WordTable.objects.create(word = word,docName = fileToken[2],freq = 1)
                if len(DocFreqTable.objects.filter(word=word))==0:
                    DocFreqTable.objects.create(word=word,docFreq = 1)
                else:
                    docIns = DocFreqTable.objects.filter(word=word)[0]
                    docIns.docFreq += 1
                    docIns.save()
            else:
                wordIns = WordTable.objects.filter(word=word,docName = fileToken[2])[0]
                wordIns.freq += 1
                wordIns.save()
            cnt += 1
            if cnt==MAX_NUM_OF_WORDS_READ:
                break
        print('\n\n Words from file '+file+'added successfully to DB!! \n\n')
                
def __main__():
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    files = []
    for dirName  in dirList:
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:]== 'txt':
                pathName = PATH_TO_DATASET+dirName+'/'+str(x)
                files.append(pathName)
    parseTextToDb(files)

def getStopWords():
    return str(loadStopWords(STOP_WORD_LIST_FILENAME))
#__main__1()