# Libraries for processing pictures
import os
import sys
import requests
import json
import pathlib

# Check Microsoft Azure settings
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v3.0/analyze"


# Which folder to check
myFolder = pathlib.Path('process')
# Search pattern for PNG pictures
myPattern = "*.png"

for myFile in myFolder.glob(myPattern):
	myReport = str(myFile) + '.txt'
	print('Processing: ' + str(myFile) + ' report: ' + myReport)
	# Read file into variable image_data, read options: binary
	myPicture = open(myFile, "rb")
	image_data = myPicture.read()
	myPicture.close()
	# Setup HTTP headers
	headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type':'application/octet-stream'}
	params = {'visualFeatures': 'Objects'}
	response = requests.post(analyze_url, headers=headers, params=params, data=image_data)
	response.raise_for_status()
	# The 'analysis' object contains various fields that describe the image. The most
	# relevant caption for the image is obtained from the 'description' property.
	analysis = response.json()
	# Save all report into text file
	mySaveFile = open(myReport, 'w')
	json.dump(analysis, mySaveFile)
	mySaveFile.close()
	print(analysis)
