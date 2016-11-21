"""
Code.Fun.Do. 2016, IIT Bombay
Team Name: DAK (Dhruv Ilesh Shah, Archit Gupta, Krish Mehta)
Project Name: Tetra

Backend Script for fetching data using the Microsoft Computer Vision API
(https://www.microsoft.com/cognitive-services/en-us/computer-vision-api).
"""

import time
import requests

import operator
import numpy as np
from bs4 import BeautifulSoup
import urllib
import webbrowser
import csv
import matplotlib.pyplot as plt
from operator import itemgetter



from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import forms
from . import models
# Create your views here.
# Variables

_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_key = 'c60ef392e53a4b96bb51304ec2463a96'  # Primary Key

_url2 = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key2 = '12b068b59d2949eeb7940e34cedbad41'

_maxNumRetries = 10
mode = "URL" # Set to URL/Local
master = [" ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0",".",",",";","!",":","(",")","{","}","[","]","/","-","=","?"]
masterMax = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","1","2","3","4","5","6","7","8","9","0"]
taboo = ["man", "outdoor", "woman", "person", "surroundings", "metal"]

def start(request):
	return render(request,'upload/index.html')
def processRequest(url, json, data, headers, params):
	"""
	Helper function to process the request to Project Oxford

	Parameters:
	json: Used when processing images from its URL.
	data: Used when processing image read from disk.
	headers: Used to pass the key information and the data type request.
	"""

	retries = 0
	result = None

	while True:

		response = requests.request(
			'post',
			url,
			json=json,
			data=data,
			headers=headers,
			params=params)

		if response.status_code == 429:

			print("Message: %s" % (response.json()['error']['message']))

			if retries <= _maxNumRetries:
				time.sleep(1)
				retries += 1
				continue
			else:
				print('Error: failed after retrying!')
				break

		elif response.status_code == 200 or response.status_code == 201:

			if 'content-length' in response.headers and int(
					response.headers['content-length']) == 0:
				result = None
			elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
				if 'application/json' in response.headers[
						'content-type'].lower():
					result = response.json() if response.content else None
				elif 'image' in response.headers['content-type'].lower():
					result = response.content
		else:
			print("Error code: %d" % (response.status_code))
			print("Message: %s" % (response.json()['error']['message']))

		break

	return result

def renderResultOnImage( result, img ):
	
	"""Display the obtained results onto the input image"""

	R = int(result['color']['accentColor'][:2],16)
	G = int(result['color']['accentColor'][2:4],16)
	B = int(result['color']['accentColor'][4:],16)

	cv2.rectangle( img,(0,0), (img.shape[1], img.shape[0]), color = (R,G,B), thickness = 25 )

	if 'categories' in result:
		categoryName = sorted(result['categories'], key=lambda x: x['score'])[0]['name']
		cv2.putText( img, categoryName, (30,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 3 )


def home(request):
	return HttpResponse("Hello")


def upload_pic(request):
	if request.method=="POST":
		print("post")
		
		image= request.POST['file']
		print("image recieved")
		return render(request,'upload/display.html',{'image':image})

	else:
		print("not post")
		form=forms.uploadform()
		return render(request,'upload/upload.html',{'form':form})

def isNormal(character):
	#master.ge
	for i in range(0, len(master)):
		if character==master[i]:
			return 1
		else:
			pass
	return 0

def isPerfect(character):
	#master.ge
	for i in range(0, len(masterMax)):
		if character==masterMax[i]:
			return 1
		else:
			pass
	return 0


def getstring(answer):
	tag = answer
	url = "http://www.goodreads.com/quotes/tag/"+tag
	r = urllib.urlopen(str(url)).read()
	soup = BeautifulSoup(r)

	#quotes=csv.writer(open("quotes.csv","w"))
	
	
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
			if isPerfect(stripped[0]):
				pool.append(stripped)
			else:
				print "ek ganda wala mila"
			#pool.append(stripped)
			#quotes.writerow([selection])
			#"""
		#print pool
		for i in range(0,len(pool)):
			minSpaces=min(minSpaces,len(pool[i]))
		#print minSpaces
		for i in range(0,len(pool)):
			#if pool[i][0]==" " or pool[i][0]==":":
			#	pass
			if len(pool[i])==minSpaces:
				selection=pool[i]
			else:
				pass
		#print selection
		return selection
	return "no"

def list(request):
	print("hello")
	if request.method=='POST':
		form=forms.uploadform(request.POST)
		newd = models.ExampleModel(model_pic = request.FILES['docfile'])
		newd.save()
		all_objects=models.ExampleModel.objects.all()
		return render(request,'upload/display.html',{'documents':all_objects})
		#return HttpResponse("Form not valid")
	else:
		form=forms.uploadform()
		return render(request,'upload/upload.html',{'form':form})

def showimage(request):
	if request.method=='POST':

		img_url = request.POST['img_url']

		rel_tag = 'nature'

		"""
		Analysis of the image retrieved via a URL
		"""
		if mode == "URL":
			# URL direction to image
			urlImage = img_url

			try:
				# Emotion API parameters
				params = None 

				headers = dict()
				headers['Ocp-Apim-Subscription-Key'] = _key2
				headers['Content-Type'] = 'application/json' 

				json = { 'url': urlImage } 
				data = None

				result = processRequest(_url2, json, data, headers, params)

				list1 = ()
				if result is not None:
					sorted(result[0]['scores'].items(), key=itemgetter(1), reverse=True)
					rel_tag = list1[0][0]
					
			except Exception, e:
				# Computer Vision parameters
				params = { 'visualFeatures' : 'Tags, Adult'} 

				headers = dict()
				headers['Ocp-Apim-Subscription-Key'] = _key
				headers['Content-Type'] = 'application/json' 

				json = { 'url': urlImage } 
				data = None

				result = processRequest(_url, json, data, headers, params )


				if result is not None:
				#	for i in range(len(result['tags'])):
				#		print result['tags'][i]['name']

				#	for i in range(len(result['tags'])):
				#		rel_tag = result['tags'][i]['name']
				#		if (rel_tag not in taboo):
				#			break
					for i in range(4):
						randit = np.random.randint(5, size=1)
						rel_tag = result['tags'][randit]['name']
						if (rel_tag not in taboo):
							break

		print rel_tag
		quote=getstring(rel_tag)

		return render(request,'upload/image.html',{'img_url':img_url,'quote':quote})

	else:
		return render(request,'upload/geturl.html')


