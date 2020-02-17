from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


#
# Routing
#

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_app_331.db"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


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

    users = User.query.all() #returns a list of class 'alchemy.User
    #print(len(users))
    print(type(users))
    print(type(users[0]))

    users_response = []
    for u in users:
        user_dict = u.__dict__
        del user_dict["_sa_instance_state"]
        users_response.append(user_dict)
    return jsonify(users_response)


@app.route("/users/create", methods=["POST"])
def create_users():
   print("CREATING A NEW USER...")
   print("FORM DATA:", dict(request.form))
   
   if "name" in request.form:
       name = request.form["name"]
       print(name)
       db.session.add(User(name=name))
       db.session.commit()
       return jsonify({"message": "CREATED OK", "name": name})
   else:
        return jsonify({"message": "OOPS PLEASE SPECIFY A NAME!"})
   
   #return jsonify({"message": "Created OK (TODO)"})


# GET /hello
# GET /hello?name=Polly
# GET /hello?name=Polly&country=USA
@app.route("/hello")
def hello(name=None):
    print("VISITING THE HELLO PAGE")
    print("REQUEST PARAMS:", dict(request.args))

    if "name" in request.args:
        name = request.args["name"]
        message = f"Hello, {name}"
    else:
        message = "Hello World"
    #return message
    return render_template("hello.html", message=message)


###FLASK_APP=app.py flask run 
# used to run the app locally
