"""
Code.Fun.Do. 2016, IIT Bombay
Team Name: DAK (Dhruv Ilesh Shah, Archit Gupta, Krish Mehta)
Project Name: Tetra

Backend Script for fetching data using the Microsoft Computer Vision API
(https://www.microsoft.com/cognitive-services/en-us/computer-vision-api).
"""

import time
import requests
import re
import operator
import numpy as np
from bs4 import BeautifulSoup
import urllib
import webbrowser
import csv
import matplotlib.pyplot as plt
from operator import itemgetter

from urlparse import urlparse
from os.path import splitext, basename

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import cv2.cv as cv
import cv2

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from . import forms
from . import models
# Create your views here.
# Variables

a=0.9
vertical=0.8

_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_key = 'c60ef392e53a4b96bb51304ec2463a96'  # Primary Key

_url2 = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
_key2 = '12b068b59d2949eeb7940e34cedbad41'

img_name = ""

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
			for tag in range(0, int(len(soup.find('body').find_all('div')[0].find_all("div", class_="quoteText")[quote].contents)/3)): 
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
			elif len(text)>50:
				continue
			"""
			for j in range(0, len(text)):
				if isNormal(text[j]):
					stripped=stripped+text[j]
				else:
					pass
			#"""
			#"""
			text=re.sub(' +',' ',text)
			text=re.sub('"','',text)
			text=text[2:]
			text=text[:-2]
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
		
			
			pool.append(text)
			#quotes.writerow([selection])
			#"""
		#print pool
		pool=sorted(pool,key=lambda x: len(x))
		#print minSpaces
		selection=[pool[0], pool[1]]
		print selection
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
	global img_name
	if request.method=='POST':

		img_url = request.POST['img_url']
		disassembled = urlparse(img_url)
		img_name, file_ext = splitext(basename(disassembled.path))
		urllib.urlretrieve(img_url, img_name)

		rel_tag = []

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
				
				
				if result is not None:
					list1 = sorted(result[0]['scores'].items(), key=itemgetter(1), reverse=True)
					rel_tag[0] = list1[0][0]
					
			except:
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
					randit = np.random.randint(5, size=1)
					while result['tags'][randit]['name'] in taboo:
						randit = np.random.randint(5, size=1)
					rel_tag.append(result['tags'][randit]['name'])
					randit = np.random.randint(5, size=1)
					while result['tags'][randit]['name'] in taboo:
						randit = np.random.randint(5, size=1)
					randit2 = np.random.randint(5, size=1)
					rel_tag.append(result['tags'][randit2]['name'])


					#if (rel_tag not in taboo):
					#	break

		print rel_tag

		for imgTag in range(0,2):
			quote=getstring(rel_tag[imgTag])
			
			print img_name
			cvImg = cv2.imread(img_name)
			H, W ,ch = cvImg.shape
			print W, H

			for option in range(0, 2):
				msg = quote[option]

				img = Image.open(img_name)
				draw = ImageDraw.Draw(img)
				font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", int(W/len(msg))+10)
				w,h = font.getsize(msg)

				#cvImg=cv2.imread("sample-out.jpg",1)
				for y in range(int(H*vertical-h*0.8), int(H*vertical+h)):
					for x in range(0, W):
						cvImg[y][x][0]=cvImg[y][x][0]*a
						cvImg[y][x][1]=cvImg[y][x][0]*a
						cvImg[y][x][2]=cvImg[y][x][0]*a
				cv2.imwrite(img_name+str(rel_tag[imgTag])+str(option)+file_ext,cvImg)

				img_loc = img_name+str(rel_tag[imgTag])+str(option)+file_ext
				img = Image.open(img_name+str(rel_tag[imgTag])+str(option)+file_ext)
				draw = ImageDraw.Draw(img)
				font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", int(W/len(msg))+10)
				draw.text(((W-w)/2, H*vertical-h/2),msg,(255,255,255),font=font)
				img.save("/home/archit/django-tutorial/tetra/upload/static/"+img_loc)

		return render(request,'upload/image.html',{'img_url':img_url,'quote':quote, 'img':img_name+str(rel_tag[0])+str(0)+file_ext, 'img1':img_name+str(rel_tag[0])+str(1)+file_ext, 'img2':img_name+str(rel_tag[1])+str(0)+file_ext, 'img3':img_name+str(rel_tag[1])+str(1)+file_ext})

		"""
			msg = quote
			img = Image.open(img_name)
			draw = ImageDraw.Draw(img)
			W, H = img.size
			font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", int(W/(len(msg)-5)))
			w, h = font.getsize(msg)
			draw.text(((W-w)/2, h/2),msg,(255,255,255),font=font)
			img_loc = img_name+file_ext
			print(img_name)
			print(file_ext)
			img.save("/home/archit/django-tutorial/tetra/upload/static/"+img_loc)
			return render(request,'upload/image.html',{'img_url':img_url,'quote':quote, 'img':img_loc})
		s"""
	else:
		return render(request,'upload/geturl.html')


