from flask import Flask, render_template, jsonify, request
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
  try:
      # Assuming the data is in JSON format, parse it
      json_data = json.loads(data)
      # Save the JSON data to a JSON file
      with open('data.json', 'w') as json_file:
          json.dump(json_data, json_file)
      return "JSON data saved successfully."
  except json.JSONDecodeError as e:
      # If the data is not in valid JSON format, save it as a text file
      with open('data.txt', 'w') as text_file:
          text_file.write(data.decode('utf-8'))
      return "Data saved as a text file."
  # the json file to save the output data
  #save_file = open("savedata.json", "w")
  #save_file.write(request.data)
  #save_file.close()


@app.route("/api/vessel/receive/get")
def VMR_GET():
  pass


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

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
