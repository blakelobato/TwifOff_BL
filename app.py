from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"


@app.route("/about")
def about():
    return "About Me Page"

@app.route("/users")
@app.route("/users.json")
def users():
    users = [
        {"id":1, "name":"First"},
        {"id":2, "name":"Second"},
        {"id":3, "name":"Third"},
    ]
    return jsonify()

###FLASK_APP=app.py flask run 
# used to run the app locally
