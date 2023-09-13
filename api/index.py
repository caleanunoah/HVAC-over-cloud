import flask

app = flask.Flask(__name__)

@app.route("/")
def ping():
    return "<p>Ping</p>"

@app.route("/sites")
def sites():
    return "<p>Sites</p>"