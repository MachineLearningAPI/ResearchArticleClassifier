"""
Created On: 29th Sept 2015
@author: Amitayush Thakur
"""

import subprocess
import os
import platform
from DatabaseParser.NaiveBayes import NaiveBayes
from DatabaseParser.wKNN import wKNN

PDF_TO_TEXT = '../xpdfbin-win-3.04/bin64/pdftotext.exe'
PDF_TO_TEXT_ubuntu = 'pdftotext'
PATH_TO_DATASET = '../TestData/'
PDF_TO_TEXT_win = '..\\xpdfbin-win-3.04\\bin64\\pdftotext.exe'
PATH_TO_DATASET_win = '..\\TestingData\\'

def testFile(path,kknResult,bayesianResult):
    i = 1
    realClass = path.split('/')[2]
    while i<8:
        classList = wKNN(path,i)
        knnResult.append((str(path)+' - '+str(i)+' - '+str(classList[0][1]),realClass,classList[0][1]))
        print(str(path)+' - '+str(i)+' - '+str(classList[0][1])+'  | '+realClass+' | '+classList[0][1])
        i += 2
    classList = NaiveBayes(path)
    bayesianResult.append((str(path)+' - '+str(classList[0][1]),realClass,classList[0][1]))
    print(str(path)+' - '+str(classList[0][1])+' | '+realClass+' | '+classList[0][1])

def testAllData():
    print('Starting The Test ....')
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    knnResult = []
    bayesianResult = []
    for dirName  in dirList:
        print('Changing Directory to '+dirName+' ...... \n\n\n')
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:] == 'pdf':
                pathName = PATH_TO_DATASET+dirName+'/'+str(x)
                testFile(pathName,knnResult,bayesianResult)
                print('File '+pathName+' has been tested!')
    cntKnn = 0
    correctCntKnn = 0    
    for res in knnResult:
        if res[1]==res[2]:
            correctCntKnn += 1
        cntKnn += 1
    correctBayes = 0
    cntBayes = 0
    for res in bayesianResult:
        if res[1] == res[2]:
            correctBayes += 1
        cntBayes += 1
    context = {
               'CorretBayes':correctBayes,
               'CntBayes' : cntBayes,
               'CorrectKNN':correctCntKNN,
               'CntKnn':cntKnn,
               }
    return context

def __main__():
    #pdfToText(PATH_TO_DATASET+'PhysicsMathematics\\'+'PhysRevLett.105.136805.pdf')
    print(str(testAllData()))

__main__()
