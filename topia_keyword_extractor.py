import sys
from topia.termextract import tag
from topia.termextract import extract
import re
num=re.compile('[^a-z]')
# if num.search('-101'):
# 	print 'ssss'
import nltk

def getkeywords(text,minoccur):
	tagger = tag.Tagger('english')
	tagger.initialize()
	 
	 # create the extractor with the tagger
	extractor = extract.TermExtractor(tagger=tagger)
	 # invoke tagging the text
	
	#s = nltk.data.load(filename,format = 'raw')
	
	# extract all the terms, even the &amp;quot;weak&amp;quot; ones
	
	extractor.filter = extract.DefaultFilter(singleStrengthMinOccur=minoccur)
	
	 # extract
	
	t= extractor(text)
	#print t
	t=[t[x][0] for x in range(len(t)) if not num.search(t[x][0]) ]
	return t

#print getkeywords("dogs dogs dogs are barking, industries, metals, therapies, therapies",3)