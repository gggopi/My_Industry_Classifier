An Industry Classifier

1. Given a website's url to find_indus() function in industry_classifer.py, the function will return the Sector in which it could possibly belong to.

2. Make sure you change all the file-paths acccordingly

3. get_info.py is the website crawler which return you a dictionary with following:
	- Name of the company
	- Description of the company (About page)
	- Meta keywords and description if the website has them
	- Address of the company

4. find_indus() uses mainly the about info of the website, gets keywords from them using Topia Keyword Extractor, map them to the graph database and finally return the Sector which carries the most weight. It can also uses the blogs of the website - and for that uncomment the lines 382 - 432 in industry_classifier.py

5.To create the graph database:
	- call tfidf_to_graph() 
	- then find_indus() with any urls list which you like

This works for 80% of the sites provided you were able to crawl and save enough data in the json files for that particular website.. 

