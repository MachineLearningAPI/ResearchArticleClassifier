"""
Created On: 20th Sept 2015
@author: Amitayush Thakur
"""

import os
from django.shortcuts import render
from django.http.response import HttpResponse
from DatabaseParser.views import parseTextToDb


# Create your views here.
PATH_TO_DATASET = 'TrainingData/'
def loadHome(request):
    return render(request,'index.html')

def showResults(request):
    context = {'serviceName':request.GET['serviceName']}
    return render(request,'results.html',context)

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