"""
Created On: 20th Sept 2015
@author: Amitayush Thakur,Jaiwant Rawat,Ashish Tilokani
"""

import os
from django.shortcuts import render
from django.http.response import HttpResponse
from DatabaseParser.views import parseTextToDb
from myapp.models import Document
from DatabaseParser.KNN import KNN


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
    k = int(request.GET['K'])
    classList =  KNN(str(document.docfile),k)
    filename = str(document.docfile)
    return HttpResponse('<br>for the file '+filename+' .The class list is: <br>'+str(classList))

def trainingDataList(request):
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    files = []
    for dirName  in dirList:
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:]== 'txt':
                pathName = '"'+PATH_TO_DATASET+dirName+'/'+str(x)+'"'
                files.append(pathName)
    context = {'msg':'The following are the files used for training!!<a href="/home/">Go back!!</a>',
               'dirList':str(dirList),
               'fileList':str(files)
               }
    return HttpResponse(context['msg']+'<br>'+context['dirList']+'<br>'+context['fileList'])

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