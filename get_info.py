import requests
from time import sleep
import geturls
import json
import re
from bs4 import BeautifulSoup
from goose import Goose

urls=['https://www.leftronic.com']
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
unwanted=re.compile('.*join.*|.*project.*|.*javascript.*|.*blog.*|.*mailto.*|.*pdf.*|.*recruit.*|.*events?.*|.*facts.*|.*mission.*|.*values.*|.*faq.*|.*news.?r?.*|.*career.*|.*updates.*|.*vision.*|.*award.*|.*products.*|.*polic(y|ies).*|.*capabilities.*|.*feedback.*|.*support.*|.*innovaitons.*',re.IGNORECASE)
lang=re.compile('.*japanese.*|.*mandarin.*|.*portuguese.*|.*germen.*|.*french.*|.*twitter.*|.*linkedin.*|.*google.*|.*youtube.*|.*facebook.*',re.IGNORECASE)
err=re.compile('.*runtime.?error.*|.*403.?.?forbidden.*|.*not.?found.*',re.IGNORECASE)
about=re.compile('.*about.*|.*Company Overview.*|.*who.we.are.*|.*what.we.do.*',re.IGNORECASE)
company=re.compile('.*company(.?overview)?.*|.*introduction.*',re.IGNORECASE)
management=re.compile('.*management.*|.*directors.*|.*team.*|.*exec.*|.*bod.*|.*leadership.*|.*staff.*|.*board.*',re.IGNORECASE)
contact=re.compile('.*contact.*',re.IGNORECASE)
boo=True
name=re.compile('([A-Z]. )?[A-Z][a-z]* ([A-Z]. )?[A-Z][a-z]*')
word_pattern = re.compile('([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+[a-z]+)?(?:\s+[A-Z][a-z]+)+)')
#self.contiguous_words = re.findall(word_pattern,self.article.text) 
depth_level=0
def get_about(url):
	sleep(3)
	desc_link=[]
	crawledLink=[]
	boo=True
	filname=url.replace('http://','')
	filname=filname.replace( 'https://','')
	filname=filname.replace('www.','')
	filname=re.sub('\..*|\/.*','',filname)
	print filname
	with open('/home/gggopi/company data/%s.json'%filname,"w") as outfile:
		def crawl(link1):
			try:
				global depth_level
				depth_level=depth_level+1
				if depth_level<=10:
					html=requests.get(link1)
					soup1=BeautifulSoup(html.content)
					for l in soup1.find_all('a'):
						l1=str(l.get('href'))
						if not linkPattern.match(l1):
							if l1[0]!='/':
								l1=url+'/'+l1
							else:
								l1=url+l1

						if (about.match(l1) or about.match(l.get_text())) and  not ( unwanted.match(l1) or unwanted.match(l.get_text())) and not lang.match(l1) and not l1 in crawledLink:
							crawledLink.append(l1)								
							if not l1 in desc_link:
								desc_link.append(l1)
							a=crawl(l1)
			except:
				print "ERROR1 with " + link1


		try:

			shtml=requests.get(url)
			desc_link=[]
			career_links=[]
			soup = BeautifulSoup(shtml.content)

			for link in soup.find_all('a'):
				link1=str(link.get('href'))
				if (about.match(link1) or about.match(link.get_text())) and not (unwanted.match(link1) or unwanted.match(link.get_text())) and not lang.match(link1):
					if not linkPattern.match(link1) :
						if link1[0]!='/':
							link1=url+'/'+link1
						else:
							link1=url+link1
					if not link1 in crawledLink:
						crawledLink.append(link1)
						depth_level=0
						desc_link.append(link1)
						a=crawl(link1)
		except:
			print "ERROR  with " + url
		print desc_link
		if len(desc_link)==0:
			try:
				shtml=requests.get(url)
				desc_link=[]
				career_links=[]
				soup = BeautifulSoup(shtml.content)
				for link in soup.find_all('a'):
					link1=str(link.get('href'))
					if (company.match(link1)) and not lang.match(link1) and not unwanted.match(link1):
						if not linkPattern.match(link1) :
							if link1[0]!='/':
								link1=url+'/'+link1
							else:
								link1=url+link1
						if not link1 in crawledLink:
							crawledLink.append(link1)
							depth_level=0
							desc_link.append(link1)
							a=crawl(link1)
				print desc_link
			except:
				print "ERROR in website: " + url
		import urllib
		import whois
		g=Goose()
		text=[]
		mem=[]
		about1={}
		new=0
		
		if len(desc_link)==0:
			desc_link.append(url)
		art=g.extract(url=url)
		
		meta={}
		meta['description']=art.meta_description
		meta['keywords']=art.meta_keywords
		about1['meta_data']=meta
		about1['name']=''
		about1['about']=''
		address={}
		try:
			d=whois.whois(url)

			address['city']=d.items()[4][1]
			address['state']=d.items()[10][1]
			address['country']=d.items()[8][1]
			address['zipcode']=d.items()[6][1]
			about1['address']=address
			about1['name']=d.items()[15][1]
		except:
			print "domain name ERROR"
		nm=re.compile('.*registrant.street.*|.*domains.by.proxy.*',re.IGNORECASE)
		if nm.match(str(about1['name'])) or not about1['name']:
			about1['name']=art.title

		for link in desc_link:
			try:
				if not boo:
					break;
				text=[]
				html = requests.get(link)    
				raw = BeautifulSoup(html.content)
				if err.match(str(raw('title'))) or err.match(str(raw('text'))):
					print "server error with "+link
					continue
				if not management.match(link) and not contact.match(link) and not unwanted.match(link)  and boo:
					print link
											
					art=g.extract(url=link)

				 	soup=BeautifulSoup(requests.get(link).content)
					for s in soup('style'):
						s.extract()
					for s in soup('script'):
						s.extract()
					for s in soup('input'):
						s.extract()	
					
					for s in soup('li'):
						if s('a') or s('link'):
							s.extract()
					for s in soup('a'):
						s.extract()	
					
					licount=len(soup.find_all('li'))
					pcount=len(soup.find_all('p'))
					tdcount=len(soup.find_all('td'))
					#print str(licount) + " " + str(pcount) + " " + str(tdcount)
						
					if (pcount>licount and pcount>tdcount):
						for p in soup.find_all(['p','li','article']):
							
							if len(p.get_text())>100 and p.name in ['p','article']:
								text.append(re.sub(r"\n+|\t+|\r+",' ',p.get_text()))
							elif p.name in ['li']:
								text.append(re.sub(r"\n+|\t+|\r+",' ',p.get_text()))
					text1=(' ').join(text)
					# print len(text1)
					text2=re.sub(r"\n+|\t+|\r+",' ',art.cleaned_text)
					# print len(text2)
					if len(text1) > len(text2):
						about1['about']=text1
					else:
						about1['about']=text2

					# print len(about1['about'])
					boo=False
					
					if not about1['about'] or len(about1['about'])<10:
						boo=True
					else:
						print about1
			except:
				print "ERROR2 with " + link
		try:
			if about1:
				json.dump(about1,outfile)

		except:
			print "json ERROR"
		#print about1
