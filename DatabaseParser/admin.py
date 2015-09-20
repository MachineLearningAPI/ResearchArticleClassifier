from django.contrib import admin
from DatabaseParser.models import WordTable, DocFreqTable, DocClass

# Register your models here.
admin.site.register(WordTable)
admin.site.register(DocFreqTable)
admin.site.register(DocClass)