from flask import Flask, render_template, jsonify

app = Flask(__name__)

babyProducts = [{
  'id': 1,
  'title': '10 Pcs Silicone Dining Set',
  'price': '$27.90',
  'description': 'For babies'
}, {
  'id': 2,
  'title': '10 Pcs Silicone Dining Set',
  'price': '$27.90',
  'description': 'For babies'
}, {
  'id': 3,
  'title': '10 Pcs Silicone Dining Set',
  'price': '$27.90',
  'description': 'For babies'
}]


@app.route("/")
def hello_jovian():
  return render_template('home.html',
                         products=babyProducts,
                         company_name='Bespojke')


@app.route("/api/jobs")
def list_jobs():
  return jsonify(babyProducts)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
