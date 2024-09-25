#-------------------------------------------------------------------------------#
# Script:   GetLatestAppDAgents.py                                              #
#                                                                               #
# Purpose:  This script is used to dowload all new agent versions from the      #
#           vendor.                                                             #
#                                                                               #
#-------------------------------------------------------------------------------#
# Amendments:                                                                   #
# Date        Who             Version   Description                             #
# ----------  --------------- --------- --------------------------------------- #
# 2024.09.23  Geoff Harrison  01.00.00  Initial version                         #
#-------------------------------------------------------------------------------#

import json
import os
from pprint import pprint
import getpass

# importing pandas package 
import pandas as pandasCSV 

import requests

# set my output path
currentPath = os.path.abspath(os.path.dirname(__file__))

# Files
AgentDataFile = currentPath+"\AppDLatestsVersions.json"
ApprovedAgentFile = currentPath+'\ApprovedAgents.txt'
outFileName = currentPath+'\latest_agents.csv'

# # get user creds
# userID = input('Enter your Cisco ID: ')
# pWord = getpass.getpass(prompt='Password: ')

# # get an OAUTH code
# # Define the URL for the OAuth token endpoint url = "https://somelink.sanitizedbyJun"
# oauthURL = "https://identity.msrv.saas.appdynamics.com/v2.0/oauth/token"
 
# # Define the payload (JSON data)
# oauthPayload = {
#   "username": userID,
#   "password": pWord,
#   "scopes": ["download"]
# }
 
# # Define headers (for JSON content)
# oauthHeaders = {
#   "Content-Type": "application/json"
# }
 
# # Send the POST request with JSON data
# requestText = "response = requests.post("+oauthURL+", headers="+json.dumps(oauthHeaders)+", data=json.dumps("+json.dumps(oauthPayload)+"))"
# print(requestText)
# response = requests.post(oauthURL, headers=oauthHeaders, data=json.dumps(oauthPayload))
 
# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the JSON response and extract the token
#     token_data = response.json()
#     print("Response:", token_data)
# else:
#     print(f"Failed to retrieve token. Status code: {response.status_code}")
#     print(response.text)

url = 'https://download.appdynamics.com/download/downloadfilelatest/'
payload = open(AgentDataFile,"w")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
# r = requests.get(url, data=payload, headers=headers)
r = requests.get(url, headers=headers)
payload.write(r.text)
#print(json.dumps(r.text))
payload.close()

# Approved Agent Data
# get the approved list into a var
approvedAgentData = open(ApprovedAgentFile, 'r')
#approvedAgents = approvedAgentData.read()
approvedAgents = list(approvedAgentData)
print(approvedAgents)

# Input vars
# jsonData = open(sys.argv[1])
jsonData = open(AgentDataFile,'r')

# Output file
if os.path.isfile(outFileName):
    # file exists, get rid of it
    os.remove(outFileName)
    
# create and start the output file
outf = open(outFileName,'a')
headingLine = 'Agent,Version,File Name,Download Path'
outf.write(headingLine+'\n')

# Parse the Agent JSON data
data = json.load(jsonData)

for i in data:
    curTitle = i['title'].strip()
    if curTitle+"\n" in approvedAgents:
        filename = i['filename'].strip()
        s3_path = i['s3_path'].strip()
        title = i['title'].strip()
        version = i['version'].strip()

        # put the data into a list and format for adding to the report file
        outputList = title,version,filename,s3_path
        printline = ','.join(outputList)

        # write the data into the CSV
        outf.write(printline+'\n')

# # Close the files
jsonData.close()
outf.close()

# Read the created CSV file into a var
csvRawData = pandasCSV.read_csv(outFileName)
  
# sort the CSV data on Agent
csvSortedData = csvRawData.sort_values(by=["Agent"], ascending=True)

# write out the sorted data to the output file
csvSortedData.to_csv(outFileName, index=False)