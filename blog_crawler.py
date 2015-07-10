import urllib2
from bs4 import BeautifulSoup
import lxml.html as html
from goose import Goose
import re
import requests
import json
# g=Goose()
# art=g.extract(url=url)
# text=art.cleaned_text.encode("utf-8")
# #print "vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv"
# print text

job=re.compile('.*blog.*|.*rss.*|.*feed.*',re.IGNORECASE)
linkPattern = re.compile("^(?:ftp|http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")
r1=re.compile('.*live.*|.*google.*|.*yahoo.*|.*subscription.*|.*login.*|.*signup.*|.*twitter.*|.*facebook.*|.*pdf.*|.*mail.*',re.IGNORECASE)

urls=[#'http://www.tataatsu.com'
#,'http://www.boostmedia.com','https://www.leftronic.com'
#,'https://www.breakthrough.com'#,'https://www.olacabs.com'
#'https://www.uber.com','https://angel.co'
#'http://www.icicibank.com'
# 'http://www.aeti.com','http://gengo.com',
# 'https://www.counsyl.com'
#,'https://cakehealth.com'
#'http://www.novogen.com',
#'http://www.cyberark.com'
# 'http://www.shell.com'
'http://www.chartindustries.com'
]


def get_blog(url):
	d= {}
	l=[]
	v={}
	name={}
	crawledLink=[]
	filname=url.replace('http://','')
	filname=filname.replace( 'https://','')
	filname=filname.replace('www.','')
	filname=re.sub('\..*|\/.*','',filname)	
	#print filname
	filename=filname+'_blog.json'	
	with open('/home/gggopi/company data/blogs/%s'%filename,"w") as outfile:
		try:
			shtml=requests.get(url)
			soup = BeautifulSoup(shtml.content)
			flag = 1
			a=[]
			blog_title=[]
			for link in soup.find_all('a'):
						link2 = str(link.get('href'))
						if not linkPattern.match(link2) and link2:
							if link2[0]!='/':
								link2=url+'/'+link2
							else:
								link2=url+link2										
						#print link2
						if link2 not in crawledLink:
							crawledLink.append(link2)
							if job.match(link2) and not r1.match(link2):
								#print 'ggggggggggggggggggggggggggggggg'
								tmp=link2.split('/')
								for t in tmp[3:]:
									if len(t)>25:
										if t in blog_title:
											break
										blog_title.append(t)
										#print 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
										a.append(link2)
										break
								shtml=requests.get(link2)
								soup2 = BeautifulSoup(shtml.content)
								for li in soup2.find_all('a'):
									li3 = str(li.get('href'))
									
									if not linkPattern.match(li3) and li3:
										if li3[0]!='/':
											li3=url+'/'+li3
										else:
											li3=url+li3										
									#print li3,'qqqqqqqqqqqqqqqqqqqqqqqqqqq'
									if not li3 in a and not r1.match(li3):
										tmp=li3.split('/')
										for t in tmp[3:]:
											if len(t)>25:
												if t in blog_title:
													break											
												blog_title.append(t)
												a.append(li3)
												break
			print a
			for li3 in a[:10]:
				#print li3
				g=Goose()
				art=g.extract(url=li3)
				d['title'] = str(art.title.encode("utf-8"))
				text=art.cleaned_text.encode("utf-8")
				d['description'] = re.sub(r"\n+|\t+|\r+",' ', str(text))
				d['link'] = li3
				if d not in l and d['description']:
					l.append(d.copy())

			v["blogs"] = l  
			print v
			json.dump(v,outfile)



		except:
			print "error with url: "+ url

# for url in urls:
# 	get_blog(url)