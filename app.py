from flask import Flask, render_template, jsonify
import http.client
import requests

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


@app.route("/api/SGTD")
def SGTD():
  API_Key = 'VJN5vqP8LfZxVCycQT6PvpJ0VM4Vk2pW'
  # Make the GET request
  url = 'https://sgtradexdummy-lbo.pitstop.uat.sgtradex.io/api/v1/config'
  r_GET = requests.get(url, headers={'SGTRADEX-API-KEY': API_Key})
  # Check the response
  if r_GET.status_code == 200:
    print("Config Data retrieved successfully!")
    #print(r_GET.text)
    #print(r_GET.json())
  else:
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

  return jsonify(r_GET)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
