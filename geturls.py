import re
from bs4 import BeautifulSoup
import requests
nasdaq=re.compile('.*nasdaq.*',re.IGNORECASE)
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
def geturl(link):
	listed_company=[]
	html=requests.get(link)
	soup1=BeautifulSoup(html.content)
	with open('list.txt','w') as outfile:

		for a in soup1.find_all('a'):
			l=str(a.get('href'))
			if not nasdaq.match(l) and linkPattern.match(l) and not l in listed_company:
				outfile.write(l+'\n')
				listed_company.append(l)
	print listed_company
	return listed_company
