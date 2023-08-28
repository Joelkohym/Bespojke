from flask import Flask, render_template, jsonify, request
import http.client
import requests
import json
import os
import sys
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

app = Flask(__name__)

babyProducts = [{
  'id': 1,
  'title': '10 Pcs Silicone Dining Set',
  'price': '$27.90',
  'description': 'For babies'
}]

DEFAULT_CONF_DIR = os.path.join(os.environ['HOME'], '.google')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

AUTHORIZATION_GUIDANCE="""
Please download Google client configuration from ENABLE GOOGLE SHEETS API button
at https://developers.google.com/sheets/api/quickstart/python to "%s"
"""

USAGE="""
Usage: python3 sheet.py 'GOOGLE_SHEET_ID' [GOOGLE_SHEET_RANGE]
Outputs contents of specified range of specified Google spreadsheet.

Setup: ./setup.sh; source *-env/bin/activate

%s

First time usage opens browser with downloaded credentials to authorize. 
""" % (AUTHORIZATION_GUIDANCE % os.path.join(DEFAULT_CONF_DIR, 'credentials.json'))






@app.route("/")
def hello_jovian():
  return render_template('home.html',
                         products=babyProducts,
                         company_name='Bespojke')


@app.route("/api/jobs")
def list_jobs():
  return jsonify(babyProducts)


@app.route("/api/sgtd")
def SGTD():
  system_ids_names = []
  API_Key = 'VJN5vqP8LfZxVCycQT6PvpJ0VM4Vk2pW'
  # Make the GET request
  url = 'https://sgtradexdummy-lbo.pitstop.uat.sgtradex.io/api/v1/config'
  r_GET = requests.get(url, headers={'SGTRADEX-API-KEY': API_Key})
  consumes_list = r_GET.json()['data']['consumes']
  # Check the response
  if r_GET.status_code == 200:
    print("Config Data retrieved successfully!")
    #print(r_GET.text)
    #print(r_GET.json())
  else:
    print(f"Failed to get Config Data. Status code: {r_GET.status_code}")
    print(r_GET.text
          )  # Print the response content if the request was not successful
  for consume in consumes_list:
    if consume['id'] == 'vessel_current_position':
      from_list = consume['from']
      for from_item in from_list:
        system_ids_names.append((from_item['id'], from_item['name']))
  return system_ids_names


@app.route("/api/vessel")
def Vessel_movement():
  API_Key = 'VJN5vqP8LfZxVCycQT6PvpJ0VM4Vk2pW'
  vessel_imo = "9702699"
  url_vessel_movement = "https://sgtradexdummy-lbo.pitstop.uat.sgtradex.io/api/v1/data/pull/vessel_movement"
  on_behalf_of_id = "49f04a6f-f157-479b-b211-18931fad4ca4"
  payload = {
    "participants": [{
      "id": "1817878d-c468-411b-8fe1-698eca7170dd",
      "name": "MARITIME AND PORT AUTHORITY OF SINGAPORE",
      "meta": {
        "data_ref_id": ""
      }
    }],
    "parameters": {
      "vessel_imo_no": vessel_imo
    },
    "on_behalf_of": [{
      "id": on_behalf_of_id
    }]
  }
  json_string = json.dumps(
    payload, indent=4)  # Convert payload dictionary to JSON string
  # Rest of the code to send the JSON payload to the API
  data = json.loads(json_string)
  response_vessel_movement = requests.post(
    url_vessel_movement, json=data, headers={'SGTRADEX-API-KEY': API_Key})
  if response_vessel_movement.status_code == 200:
    print(f"Response JSON = {response_vessel_movement.json()}")
    print("Pull vessel_movement success.")
  else:
    print(
      f"Failed to PULL vessel_movement data. Status code: {response_vessel_movement.status_code}"
    )
    print(response_vessel_movement.text)
  return response_vessel_movement.text


@app.route("/api/vessel/receive", methods=['POST'])
def Vessel_movement_receive():
  data = request.data  # Get the raw data from the request body
  # Assuming the data is in JSON format, parse it
  #json_data = json.loads(data)
  # Save the JSON data to a JSON file
  print(data)
  #carry gsheet writing
  
  return "Data saved as a text file."

@app.route("/api/vessel/receive/get")
def VMR_GET():
  pass

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
