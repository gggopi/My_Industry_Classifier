import re
from bs4 import BeautifulSoup
import requests
import json
nasdaq=re.compile('.*nasdaq.*',re.IGNORECASE)
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")



def get_filenames_with_industry(link):
	listed_company={}
	html=requests.get(link)
	soup1=BeautifulSoup(html.content)
	try:
		with open("url_industry_list.json","r") as outfile:
			listed_company=json.load(outfile)
			outfile.close()
	except:
		print "file : url_industry_list does not exist"
	with open("url_industry_list.json","w") as outfile:
		for a in soup1.findAll('td'):
			if a.findChild():
				l=str(a.findChild().get('href'))
				if not nasdaq.match(l) and linkPattern.match(l):
					url=str(a.findChild().get('href'))
					filname=url.replace('http://','')
					filname=filname.replace( 'https://','')
					filname=filname.replace('www.','')
					# filname=filname.replace('.com','') 
					# filname=filname.replace( '.org','')
					# filname=filname.replace( '.gov','')
					filname=re.sub('\..*|\/.*','',filname)
					ind=str(a.findNextSiblings(style='width:105px')[0].get_text())
					#outfile.write(l+'\n')
					if filname not in listed_company:
						listed_company[filname]=ind
		json.dump(listed_company , outfile)
	#return listed_company
	print listed_company

get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&industry=Capital+Goods&pagesize=500')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Finance')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Energy')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Health+Care')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Technology')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Public+Utilities')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Consumer+Services')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&pagesize=500&industry=Transportation')
get_filenames_with_industry('http://www.nasdaq.com/screening/companies-by-region.aspx?region=North+America&industry=Basic+Industries&pagesize=300')
