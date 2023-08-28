from flask import Flask, render_template, jsonify
import http.client
import requests
import json

app = Flask(__name__)

babyProducts = [{
  'id': 1,
  'title': '10 Pcs Silicone Dining Set',
  'price': '$27.90',
  'description': 'For babies'
}]
# }, {
#   'id': 2,
#   'title': '10 Pcs Silicone Dining Set',
#   'price': '$27.90',
#   'description': 'For babies'
# }, {
#   'id': 3,
#   'title': '10 Pcs Silicone Dining Set',
#   'price': '$27.90',
#   'description': 'For babies'
# }]


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
  API_Key = 'VJN5vqP8LfZxVCycQT6PvpJ0VM4Vk2pW'
  # Make the GET request
  url = 'https://sgtradexdummy-lbo.pitstop.uat.sgtradex.io/api/v1/config'
  r_GET = requests.get(url, headers={'SGTRADEX-API-KEY': API_Key})
  # Check the response
  if r_GET.status_code == 200:
    response = "Config Data retrieved successfully!"
    print("Config Data retrieved successfully!")
    #print(r_GET.text)
    #print(r_GET.json())
  else:
    response = "Config Data failed successfully!"
    print(f"Failed to get Config Data. Status code: {r_GET.status_code}")
    print(r_GET.text
          )  # Print the response content if the request was not successful


#   conn =     http.client.HTTPSConnection('bespojke.com/api/sgtd')
#   conn.request("POST", "/", '''{
#   "test": "event"
# }''', {'Content-Type': 'application/json'})
#   # Get the HTTP response
#   connResponse = conn.getresponse();
# # Read the HTTP response
#   response     = connResponse.read();
# # Print the HTTP response
#   print(response);

  return response


@app.route("/api/vessel")
def Vessel_movement():
  API_Key = 'VJN5vqP8LfZxVCycQT6PvpJ0VM4Vk2pW'
  # Make the GET request
  url = 'https://sgtradexdummy-lbo.pitstop.uat.sgtradex.io/api/v1/config'
  r_GET = requests.post(url, headers={'SGTRADEX-API-KEY': API_Key})
  # Check the response
  if r_GET.status_code == 200:
    response = "Config Data retrieved successfully!"
    print("Config Data retrieved successfully!")
    #print(r_GET.text)
    #print(r_GET.json())
  else:
    response = "Config Data failed successfully!"
    print(f"Failed to get Config Data. Status code: {r_GET.status_code}")
    print(r_GET.text
          )  # Print the response content if the request was not successful
  consumes_list = r_GET.json()['data']['consumes']
  system_ids_names = []
  vessel_imo = "9702699"

  #===================PULL======================================
  for consume in consumes_list:
    if consume['id'] == 'vessel_current_position':
      from_list = consume['from']
      for from_item in from_list:
        system_ids_names.append((from_item['id'], from_item['name']))
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


#   conn =     http.client.HTTPSConnection('bespojke.com/api/sgtd')
#   conn.request("POST", "/", '''{
#   "test": "event"
# }''', {'Content-Type': 'application/json'})
#   # Get the HTTP response
#   connResponse = conn.getresponse();
# # Read the HTTP response
#   response     = connResponse.read();
# # Print the HTTP response
#   print(response);

  return response_vessel_movement.json()

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
