def NaiveBayes(file):
    fp = open(file,'r')
    wordList = fp.read().split()
    termFreq={} #dictionary for holding the words which occur in the test document
	
    for word in wordList:
        termFreq[word]=1
	
    #(term, docFrequency) pairs    
    keyWords=DocFreqTable.objects.all() 	
	
    #List of all classes
    classes = DocClass.objects.order_by.values('className').distinct()
	
    #number of classes
    numClass=len(classes)
    
    #(document, class) pairs
	docTemp = DocClass.objects.all()
	
    #number of documents
	docCount = len(doctemp)
    
    #(probability,class) pairs
    scores=[]    
     
	#Outer Loop: for every class
	for clas in classes: 
        
        #probClass is P(clas) - probability of clas
	    probClassCount = DocClass.objects.filter(className = clas)
	    probClass = len(probClassCount)/docCount
	   
        prob = probClass #prob is the probability of the test document of belonging to clas
       
        #Inner Loop: for every term
	    for tup in keyWords: #keywords-(word,document frequency)
            
            keys = tup.word
            t = 0 
		  
            #t=1, whether in test document
            if termFreq[keys]:
                t = 1 
          
            listkey = WordTable.objects.filter(word=keys)
          
            #zero probability removal
            countkeys = 1  
          
            for listkeytup in listkey: 
                countkeys += len(DocClass.objects.filter(docName= listkeytup.docName))  
          
            if t==1:  
                prob= prob * countKeys/(probClassCount+numClass)
            else:
                prob= prob * (1-(countKeys/(probClassCount+numClass))
            
        score.append( (-prob,clas) )        
       
    score.sort()
    
    #make the probabilities non negative again    
    for i in score:
        i[0]*=-1;
           
    return score