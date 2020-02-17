from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"


@app.route("/about")
def about():
    return "About me page"

###FLASK_APP=app.py flask run 
# used to run the app locally
