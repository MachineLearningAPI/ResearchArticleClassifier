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

def KNN(file,k):
	fp = open(file,'r')
    wordList = fp.read().split()
	termFreq={}

	den1=0	
		
    for word in wordList:
        termFreq[word] +=1
	
	docCount=len(DocClass.objects.all())
	
	tfidf_file={}
	
	for key in termFreq:
		docFreq=DocFreqTable.objects(word=key)[0]
		tf=termFreq[key]
		idf=log10(docCount/docFreq)
		den1+=(tf*idf)**2
		tfidf_file[key]=tf*idf
		
	docIns = DocClass.objects.all()
	
	#(cosing similarity, Class) list
	scores=[]
	
	den1=sqrt(den1)	
	
	#traversing over all documents
	for doc in docIns:
		doc_name=doc.docName
		docClass=DocClass.objects.filter(docName = doc_name)
		
		#all words of this document
		termDocFreq=WordTable.objects.filter(docName = doc_name)
		
		#numerator of cosine similarity function
		num=0
		
		den2=0
		
		#iterating over all terms in doc_name
		for row in termDocFreq:
			
			word=row.word 	
		
			docFreq=DocFreqTable.objects(word=word)[0]
			tf=termFreq[key]
			idf=log10(docCount/docFreq)
			den2+=(tf*idf)**2
			
			if word in termFreq.keys():
				num+=tfidf_file[word]*(tf*idf) 
		
		den2=sqrt(den2)	
	
		cosineSim=num/(den1*den2)
		
		score.append( (cosineSim,docClass) )
		
	score.sort()
	
	classCount={}
	
	for score_elem in score:
		if k == 0:
			break
		classCount[ score_elem[1] ]+=1
		k-=1
	
	tempResult=[]
	
	for key in classCount.keys()
		tempResult.append( (classCount[key],key) )	
	
	tempResult.sort()
	
	for tup in tempResult:
		result.append(tup[1])
	
	return result