"""
Created On: 20th Sept 2015
@author: Amitayush Thakur,Jaiwant Rawat,Ashish Tilokani
"""

import os
from django.shortcuts import render
from django.http.response import HttpResponse
from DatabaseParser.views import parseTextToDb, getStopWords
from myapp.models import Document
from DatabaseParser.wKNN import wKNN
from DatabaseParser.NaiveBayes import NaiveBayes
from DatabaseParser.views import filterStopWords 
from DatabaseParser.testData import testAllData

# Create your views here.
PATH_TO_DATASET = 'TrainingData/'
def loadHome(request):
    return render(request,'index.html')

def showResults(request):
    context = {}
    if request.GET['serviceName']=='TestingKNN':
        context = {'serviceName':request.GET['serviceName'],'algoName':'KNN'}
    else:
        context = {'serviceName':request.GET['serviceName'],'algoName':'Bayesian'}
    return render(request,'test.html',context)

def applyKNN(request):
    #get the file on which we will be applying
    docList = Document.objects.all()
    l = len(docList)
    revDocList = []
    i = 0
    while i<l:
        revDocList.append(docList[l-i-1])
        i += 1
    document = revDocList[0]
    if request.GET['K']!='' :
        k = int(request.GET['K'])
    else:
        k = 7
    classList =  wKNN(str(document.docfile),k)
    l = len(classList)
    lis = []
    for i in range(l):
        lis.append((classList[i][1],classList[i][0]))
    filename = str(document.docfile)
    context = {
               'title':'KNN Results',
	       'msg':'<br>For the file '+filename+' .<a href="/home/">Click here to go back!!</a>',
	       'colA':'Class Name',
	       'colB':'Percentage Chance',
               'dataSet' : lis,
               }
    return render(request,'results.html',context)

def trainingDataList(request):
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    files = []
    for dirName  in dirList:
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:]== 'txt':
                pathName = '"'+PATH_TO_DATASET+dirName+'/'+str(x)+'"'
                files.append(pathName)
    l = len(files)
    lis = []
    for i in range(l):
        lis.append((i+1,files[i]))
    context = {
               'title':'Training Data Used',
	       'msg':'The following are the files used for training!!<a href="/home/">Go back!!</a>',
	       'colA':'SL.No.',
	       'colB':'Filename',
               'dataSet' : lis,
               }
    return render(request,'results.html',context)

def populateWordDb(request):
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    files = []
    for dirName  in dirList:
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:]== 'txt':
                pathName = PATH_TO_DATASET+dirName+'/'+str(x)
                files.append(pathName)
    parseTextToDb(files)
    return HttpResponse("All words Added!!!")

def callBayesian(request):
    docList = Document.objects.all()
    l = len(docList)
    revDocList = []
    i = 0
    while i<l:
        revDocList.append(docList[l-i-1])
        i += 1
    document = revDocList[0]
    classList =  NaiveBayes(str(document.docfile))
    l = len(classList)
    lis = []
    for i in range(l):
        lis.append((classList[i][1],classList[i][0]))
    filename = str(document.docfile)
    context = {
               'title':'Bayesian Results',
	       'msg':'<br>For the file '+filename+' .<a href="/home/">Click here to go back!!</a>',
	       'colA':'Class Name',
	       'colB':'Log10(Probability)',
               'dataSet' : lis,
               }
    return render(request,'results.html',context)

def loadTextFile(request):
    filename = request.GET['file']
    fp = open(filename,encoding="latin-1")
    content = fp.read()
    fp.close()
    return HttpResponse(content, content_type='text/plain')

def getStop(request):
    return HttpResponse(getStopWords())

def removeStopWords(request):
    filterStopWords()
    return HttpResponse("StopWords Removed !!!")

def testAll(request):
    context = testAllData()
    return render(request,'results.html',context)
