from flask import Blueprint, jsonify, request, render_template, current_app
from web_app.models import User, Tweet, db
#from web_app.twitter_service import twitter_api_client

my_routes = Blueprint("my_routes", __name__)

@my_routes.route("/tweets")
@my_routes.route("/tweets.json")
def tweets():
    tweets = Tweet.query.all() #returns a list of class 'alchemy.User
    #print(len(users))
    print(type(tweets))
    print(type(tweets[0]))

    tweets_response = []
    for t in tweets:
        tweets_dict = t.__dict__
        del tweets_dict["_sa_instance_state"]
        tweets_response.append(tweets_dict)
    return jsonify(tweets_response)


@my_routes.route("/tweets/create", methods=["POST"])
def create_tweets():
    print("CREATING A NEW TWEET..")
    print("FORM DATA:", dict(request.form))

    if "status" in request.form:
        tweet = request.form["status"]
        print(tweet)
        db.session.add(Tweet(status=tweet))
        db.session.commit()
        return jsonify({"message": "CREATED OK", "tweet": tweet})
    else:
        return jsonify({"message": "OOPS PLEASE SPECIFY A tweet!"})


@my_routes.route("/")
def index():
    #return "Hello World!"
    return render_template("homepage.html")


@my_routes.route("/about")
def about():
    return "About Me Page"


@my_routes.route("/users")
@my_routes.route("/users.json")
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


@my_routes.route("/users/create", methods=["POST"])
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

@my_routes.route("/get_tweets")
def get_tweets():
    print(tweets)
    return jsonify({"message": "OK"})
# GET /hello
# GET /hello?name=Polly
# GET /hello?name=Polly&country=USA
@my_routes.route("/hello")
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