from bs4 import BeautifulSoup
import urllib
import webbrowser
import csv

tag = "water"
url = "http://www.goodreads.com/quotes/tag/"+tag
r = urllib.urlopen(str(url)).read()
soup = BeautifulSoup(r)

quotes=csv.writer(open("quotes.csv","w"))

master = [" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0",".",",",";","!",":","(",")","{","}","[","]","/","-","=","?"]
def isNormal(character):
	#master.ge
	for i in range(0, len(master)):
		if character==master[i]:
			return 1
		else:
			pass
	return 0

#print r
if len(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText"))>0:
	pool=[]
	print len(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText"))
	for quote in range(0,len(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText"))):
		tags=0
		fullText=""
		for tag in range(0, len(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText")[quote].contents)): 
			if str(type(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText")[quote].contents[tag]))=="<class 'bs4.element.NavigableString'>":
				fullText=fullText+soup.find('body').find_all('div')[0].find_all("div", class_="quoteText")[quote].contents[tag].encode('ascii','ignore')
				tags=tags+1	
		#print tags
		text = soup.find('body').find_all('div')[0].find_all("div", class_="quoteText")[quote].contents[0].encode('ascii','ignore')	
		text=fullText
		#print text
		stripped=""
		flag=0
		if len(text)<10:
			continue
		"""
		for j in range(0, len(text)):
			if isNormal(text[j]):
				stripped=stripped+text[j]
			else:
				pass
		#"""
		#"""
		for j in range(0,len(text)):
			if isNormal(text[j]):
				if text[j]==" " and flag==0:
					pass 
				else:
					flag=1
					if text[j]==",":
						stripped=stripped+".."
					else:
						stripped=stripped+str(text[j])
		#"""
		#print stripped[0], stripped[len(stripped)-1], len(stripped) 
		#print stripped
		#numSpaces=0
		minSpaces=500
		selection=""
		"""
		for i in range(0, len(stripped)):
			if stripped[i]==" ":
				numSpaces=numSpaces+1
			else:
				pass
			pool.append([stripped,numSpaces])
		print len(pool)
		for i in range(0, len(pool)):
			minSpaces=min(minSpaces, pool[i][1])
		for i in range(0, len(pool)):
			if pool[i][1]==minSpaces:
				selection=pool[i][0]
		"""
		pool.append(stripped)
		quotes.writerow([selection])
		#"""
	#print pool
	for i in range(0,len(pool)):
		minSpaces=min(minSpaces,len(pool[i]))
	#print minSpaces
	for i in range(0,len(pool)):
		if len(pool[i])==minSpaces:
			selection=pool[i]
		else:
			pass
	print selection

#print type(soup.find('body').find_all("div")[0].find_all("div", class_="quoteText")[0])
#print len(soup.find('body').find_all("div", class_="content").find_all("div", class_=quoteText))
#print(type(soup))
#print(soup.find_all('a'))
