"""
Created: 20th Sept 2015
@author: Jaiwant, Amitayush Thakur
"""
from django.db import models


MAX_LEN = 256
DEFAULT_FIELD_VALUE = ""
"""
    This class is meant for extracting word frequencies
"""

class WordTable(models.Model):
    word = models.CharField(primary_key=False,max_length=MAX_LEN,null=False,default=DEFAULT_FIELD_VALUE)  #Primary Key
    docName = models.CharField(primary_key=False,max_length=MAX_LEN,null=False,default=DEFAULT_FIELD_VALUE)
    freq = models.IntegerField(null=False,default=0)
    def __str__(self):
        """ __str__()- returns the name of the user """
        return self.word +' - ' +self.docName


class DocFreqTable(models.Model):
    word = models.CharField(primary_key=False,max_length=MAX_LEN,null=False,default=DEFAULT_FIELD_VALUE)  #Primary Key
    docFreq = models.IntegerField(null=False,default=0)
    def __str__(self):
        """ __str__()- returns the name of the user """
        return self.word +' - ' +str(self.docFreq)
    
class DocClass(models.Model):
    docName = models.CharField(max_length=MAX_LEN,null=False,default=DEFAULT_FIELD_VALUE)
    className = models.CharField(max_length=MAX_LEN,null=False,default=DEFAULT_FIELD_VALUE)
    def __str__(self):
        return self.docName+' - '+self.className
