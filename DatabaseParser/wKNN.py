'''
Created on Sep 24, 2015

@author: Amitayush Thakur
'''
import numpy as numpy
import math as math
from DatabaseParser.models import DocFreqTable, DocClass, WordTable
from DatabaseParser.views import MAX_NUM_OF_WORDS_READ
from DatabaseParser.views import FREQ_THRESHOLD_PERCENT

class Tuple:
    def __init__(self):
        self.list = []
        self.count = 0
    def add(self,elem):
        self.list.append(elem)
        self.count += 1
    def distance(self,other):
        myVector = numpy.asarray(self.list)
        otherVector = numpy.asarray(other.list)
        if self.count == other.count:
            M11 = numpy.sum(myVector & otherVector)
            M01_M10 = numpy.sum(myVector ^ otherVector)
            return (M01_M10)/(M11+M01_M10)
        else:
            return 0
    def norm(self):
        myVector = numpy.asarray(self.list)
        return math.sqrt(numpy.sum(myVector**2))
    def __str__(self):
        return str(self.list)

def onlyascii(char):
    if ord(char) < 48 or ord(char) > 127: return ''
    else: return char
    
def getASCII(inputString):
    l = len(inputString)
    i = 0
    newStr = ''
    while i<l:
        newStr += onlyascii(inputString[i])
        i += 1
    return newStr.lower()

def getTuple(wordList,fileKeyWords):
    tup = Tuple()
    for word in wordList:
        if word in fileKeyWords.keys():
            tup.add(1)
        else:
            tup.add(0)
    return tup

def wKNN(file,k):
    NUM_OF_DOCS = DocClass.objects.count()
    FREQ_THRESHOLD = NUM_OF_DOCS*FREQ_THRESHOLD_PERCENT
    #get all rows with frequency more than threshold
    docInstances = DocFreqTable.objects.filter(docFreq__lte = FREQ_THRESHOLD)
    numDocInstances = len(docInstances)
    wordList = []
    for inst in docInstances:
        wordList.append(getASCII(inst.word))
    #Now start reading the file and then parse it match if the keywords are present in the file
    filePointer = open(file,encoding="latin-1")
    #Push the keywords in the file to a dictionary datastructure
    fileKeyWords = {}
    wordsInFile = None
    wordsInFile = filePointer.read().split()
    """try:
                    wordsInFile = filePointer.read().split()
                except:
                    for line in filePointer:
                        wordsInLine = None
                        try:
                            wordsInLine = line.split()
                        except:
                            wordsInLine = ''
                        for word in wordsInLine:
                            wordsInFile.append(word)"""
    cnt = 0
    for word in wordsInFile:
        fileKeyWords[getASCII(word)] = True
        cnt += 1
        if cnt == MAX_NUM_OF_WORDS_READ:
            break
    #Get the tupple for the current file
    inputFileTupple = getTuple(wordList,fileKeyWords)
    docListInstance = DocClass.objects.all()
    docList = []
    # to get back the class name for any given document (assuming the number of documnets can be stored in the main mememory)
    docToClassName = {} 
    for inst in docListInstance:
        docList.append(inst.docName)
        docToClassName[inst.docName] = inst.className
    numRows = len(docList)
    numCols = len(wordList)
    knnMat = matrix = [[0]*numCols for i in range(numRows)]
    rowNumber = 0
    for doc in docList:
        docWordInstances = WordTable.objects.filter(docName=doc)
        docKeyWords = {}
        for wordInstance in docWordInstances:
            docKeyWords[wordInstance.word] = True
        oneRow = getTuple(wordList,docKeyWords).list
        x = 0
        while x<numCols:
            knnMat[rowNumber][x] = oneRow[x]
            x += 1
        rowNumber += 1
    #get all the distance from the doc
    distanceClassList = []
    i = 0
    while i < numRows:
        newTuple = Tuple()
        newTuple.list = knnMat[i]
        newTuple.count = numCols
        dis  = inputFileTupple.distance(newTuple)
        distanceClassList.append((dis,docToClassName[docList[i]]))
        i += 1
    distanceClassList.sort()
    classCount = {}
    cnt = 0
    for ins in distanceClassList:
        wt = 1/(ins[0]+0.01) #for removing the zero error
        if ins[1] in classCount.keys():
            classCount[ins[1]] += wt
        else:
            classCount[ins[1]] = wt
        if cnt == k:
            break;
        cnt += 1
    classCountList = []
    for className in classCount.keys():
        classCountList.append((-1*classCount[className],className))
    classCountList.sort()
    answer_list = []
    len_classCountList = len(classCountList)
    sum_rows = 0
    i = 0
    while i < len_classCountList:
        sum_rows += classCountList[i][0]
        i += 1
    i = 0
    while i < len_classCountList:
        answer_list.append(((classCountList[i][0]/(sum_rows))*100,classCountList[i][1]))
        i += 1
    return answer_list
