from DatabaseParser.models import DocClass, DocFreqTable, WordTable
import math

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

def dis_formula(tfidf_file,termFreq,docCount):
    den1 = 0
    docFreq = 1
    for key in termFreq:
        docIns = DocFreqTable.objects.filter(word=key)
        if len(docIns)==0:
            continue;
        else:
            docFreq = docIns[0].docFreq
        tf= termFreq[key]
        idf = math.log10(docCount/docFreq)
        den1 += (tf*idf)**2
        tfidf_file[key] = tf*idf
    return math.sqrt(den1)

def KNN(file,k):
    fp = open(file,'r')
    wordList = fp.read().split()
    termFreq={}
    for word in wordList:
        word = get_my_string(word)
        if word in termFreq.keys():
            termFreq[word] +=1
        else:
            termFreq[word] = 1
    docCount=len(DocClass.objects.all())
    tfidf_file={}
    den1 = dis_formula(tfidf_file,termFreq,docCount)
    docIns = DocClass.objects.all()
    #(cosing similarity, Class) list
    scores=[]
    #traversing over all documents and computing the tfid for each document
    #also we compute the cosineSimilarity
    for doc in docIns:
        doc_name = doc.docName
        docClass = doc.className
        #all words of this document
        termDocFreq = WordTable.objects.filter(docName = doc_name)
        #numerator of cosine similarity function
        num=0
        den2=0
        #iterating over all terms in doc_name
        for row in termDocFreq:
            word = row.word
            docFreq = 1
            docIns = DocFreqTable.objects.filter(word=word)
            if len(docIns)==0:
                continue;
            else:
                docFreq = docIns[0].docFreq
            tf = row.freq
            idf = math.log10(docCount/docFreq)
            den2 += (tf*idf)**2
            if word in termFreq.keys():
                num += tfidf_file[word]*(tf*idf) 
            den2 = math.sqrt(den2)	
        cosineSim = num/(den1*den2)
        scores.append( (-1*cosineSim,docClass) )
    scores.sort()
    classCount={}
    for score_elem in scores:
        if k == 0:
            break
        if score_elem[1] in classCount.keys():
            classCount[ score_elem[1] ] += 1
        else:
            classCount[score_elem[1]] = 1
        k -= 1
    tempResult=[]
    for clas in classCount.keys():
        tempResult.append( (-1*classCount[clas],clas) )	
    tempResult.sort()
    return tempResult