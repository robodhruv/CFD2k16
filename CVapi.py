"""
Code.Fun.Do. 2016, IIT Bombay
Team Name: DAK (Dhruv Ilesh Shah, Archit Gupta, Krish Mehta)
Project Name: Tetra

Backend Script for fetching data using the Microsoft Computer Vision API
(https://www.microsoft.com/cognitive-services/en-us/computer-vision-api).
"""

import time
import requests
import cv2
import operator
import numpy as np


import matplotlib.pyplot as plt


# Variables

_url = 'https://api.projectoxford.ai/vision/v1/analyses'
_key = 'c60ef392e53a4b96bb51304ec2463a96'  # Primary Key
_maxNumRetries = 10
mode = "URL" # Set to URL/Local


def processRequest(json, data, headers, params):
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
			_url,
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

result = ""

"""
Analysis of the image retrieved via a URL
"""
if mode == "URL":
	# URL direction to image
	urlImage = 'http://images4.fanpop.com/image/photos/18700000/Cool-Desert-LandScape-fullmetal-alchemist-manga-18757117-1024-768.jpg'

	# Computer Vision parameters
	params = { 'visualFeatures' : 'Tags, Adult'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/json' 

	json = { 'url': urlImage } 
	data = None

	result = processRequest( json, data, headers, params )

else:
	# Load raw image file into memory
	pathToFileInDisk = r'D:\tmp\3.jpg'
	with open( pathToFileInDisk, 'rb' ) as f:
		data = f.read()
		
	# Computer Vision parameters
	params = { 'visualFeatures' : 'Color,Categories'} 

	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream'

	json = None

	result = processRequest( json, data, headers, params )

if result is not None:
	for i in range(len(result['tags'])):
		print (result['tags'][i]['name'])