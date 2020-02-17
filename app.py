from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    #return "Hello World!"
    return render_template("homepage.html")


@app.route("/about")
def about():
    return "About Me Page"

@app.route("/users")
@app.route("/users.json")
def users():
    users = [
        {"id":1, "name": "First"},
        {"id":2, "name": "Second"},
        {"id":3, "name": "Third"},
    ]
    return jsonify(users)

@app.route("/users/create", methods=["POST"])
def create_users():
   print("CREATING A NEW USER...")
   print("FORM DATA:", dict(request.form))
   #todo:create a new user
   return jsonify({"message": "Created OK (TODO)"})










###FLASK_APP=app.py flask run 
# used to run the app locally
