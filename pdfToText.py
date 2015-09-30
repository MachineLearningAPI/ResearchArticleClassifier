"""
Created On: 20th Sept 2015
@author: Amitayush Thakur,Jaiwant Rawat,Ashish Tilokani
"""

import subprocess
import os
import platform

PDF_TO_TEXT = '../xpdfbin-win-3.04/bin64/pdftotext.exe'
PDF_TO_TEXT_ubuntu = 'pdftotext'
PATH_TO_DATASET = 'TestData/'
PDF_TO_TEXT_win = '..\\xpdfbin-win-3.04\\bin64\\pdftotext.exe'
PATH_TO_DATASET_win = '..\\TestData\\'

def pdfToText(path):
    if platform.system()=='Linux':
        subprocess.call([PDF_TO_TEXT_ubuntu,path])
    else:
        subprocess.call([PDF_TO_TEXT,path])


def convertTextToPDF():
    print('Conversion starting ....')
    dirList = [x for x in os.listdir(PATH_TO_DATASET)]
    files = []
    for dirName  in dirList:
        print('Changing Directory to '+dirName+' ...... \n\n\n')
        for x in os.listdir(PATH_TO_DATASET+dirName):
            if str(x)[-3:] == 'pdf':
                pathName = PATH_TO_DATASET+dirName+'/'+str(x)
                files.append(pathName)
                pdfToText(pathName)
                print('File '+pathName+' has been converted')
    context = {
               'dirList':str(dirList),
               'fileList':str(files)
               }
    return context

def __main__():
    #pdfToText(PATH_TO_DATASET+'PhysicsMathematics\\'+'PhysRevLett.105.136805.pdf')
    print(str(convertTextToPDF()))

__main__()