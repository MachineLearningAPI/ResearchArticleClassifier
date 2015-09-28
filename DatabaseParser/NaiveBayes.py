'''
Created on Sep 22, 2015

@author: Ashish Tilokani, Jaiwant Rawat
'''
import sys

from DatabaseParser.models import DocFreqTable, DocClass, WordTable
from DatabaseParser.views import FREQ_THRESHOLD_PERCENT
from DatabaseParser.views import MAX_NUM_OF_WORDS_READ
from math import log10

def NaiveBayes(file):
    
    #Logging to a file
    orig_stdout = sys.stdout
    f = open('out.txt', 'w')
    sys.stdout = f
    
    #Extract tokens from doc
    #1. Select the first 300 words which
    #2. Contains only letters (helps in removing meaningless tokens)
    #3. Must not be a stop word
    fp = open(file,'r')
    docCount = DocClass.objects.count()
    print("Number of documents: ",docCount)
    FREQ_THRESHOLD = docCount*FREQ_THRESHOLD_PERCENT   
    
    W = fp.read().split()
    cnt=0
    processedW={}
    for w_ in W:
        w=w_.lower()
        if not w.isalpha():
            continue
        if w in processedW.keys(): 
            continue
        #term occurs in a lot of documents
        if DocFreqTable.objects.filter(docFreq__gte = FREQ_THRESHOLD,word=w).count()==1:
            continue
        
        processedW[w]=1
        cnt += 1
        if cnt == MAX_NUM_OF_WORDS_READ:
            break
    
    #List of all (className: "className") key value pairs
    C = DocClass.objects.all().values('className').distinct()
    #number of classes
    countC=len(C)
    
    print("Number of classes: ",countC)

    #(probability,class) pairs
    scores=[]
    
    #number of terms
    B=DocFreqTable.objects.all().count()   
    
    print("Number of terms: ",B) 
    
    #Outer Loop: for every class
    for c in C: 
        
        cName=c['className']
        
        print("Calculating probabilities for class=",cName)
        
        #get all docs corresponding to current class
        docsC = DocClass.objects.filter(className = cName).values("docName")
        priorC = len(docsC)/docCount
        prob = log10(priorC) #prob is the probability of the test document of belonging to clas
        
        #number of docs of current class in which a term of vocabulary cumulative for all terms
        denC = WordTable.objects.filter(docName__in=docsC).count()
        
        #Inner Loop: for every term
        for t in processedW.keys():
            
            #number of docs of current class in which the current term appears
            numC = WordTable.objects.filter(docName__in=docsC,word=t).select_related().count()
            
            print("Using term=",t)
            
            #how much evidence does term provide that clas is the correct class        
          
            prob= prob + log10( (1+numC)/(denC+B) )                
                                     
        scores.append( (-prob,cName) )        
       
    scores.sort()
    
    answer_list = []
    
    #make the probabilities non negative again    
    for i in scores:
        answer_list.append( ( -i[0], i[1] ) );
    
    sys.stdout = orig_stdout
    f.close()
           
    return answer_list
