from flask import Blueprint, jsonify, request, render_template, flash
from sklearn.linear_model import LogisticRegression
#import random forest, xgboost, etc. when we make data science attribute
import numpy as np

from web_app.models import User, Tweet, db
from web_app.twitter_service import twitter_api_client
from web_app.basilica_service import basilica_connection

new_routes = Blueprint("new_routes", __name__)

client = twitter_api_client()
basilica_client = basilica_connection()

@new_routes.route("/")
def index():
    """Returns our homepage layout when opening the app"""
    return render_template("homepage.html")


#
# DATABASE & EMBEDDING 
#

@new_routes.route("users")
@new_routes.route("/users.json")
def list_users():
    print("Here's a List of Users!")
    users = User.query.all() #this will return a list of class 'alchemy.User' from models.py
    print(len(users))

    users_response = []
    for u in users:
        user_dict = u.__dict__
        del user_dict["_sa_instance_state"]
        users_response.append(user_dict)
    return jsonify(users_response)


@new_routes.route("/users/<string:screen_name>")
def show_user(screen_name=None):
    print("User:", screen_name)
    try:
        # Get user information from Twitter
        twitter_user = client.get_user(screen_name)
        #print(type(twitter_user))

        #find or create db_user 
        db_user = User.query.get(twitter_user.id) or User(id = twitter_user.id)
        print(db_user)

        # Update the User Database
        db_user.screen_name = twitter_user.screen_name
        db_user.followers_count = twitter_user.followers_count
        db.session.add(db_user)
        db.session.commit()


        # Get Tweets now:
        statuses = client.user_timeline(screen_name, tweet_mode = "extended", count=50, exclude_replies=True, include_rts=False)
        for status in statuses:
            print(status.full_text)
            # Find or create a database tweet
            db_tweet = Tweet.query.get(status.id) or Tweet(id = status.id)
            print(db_tweet)
            # Update database tweet
            db_tweet.user_id = status.author.id 
            db_tweet.full_text = status.full_text
            embedding = basilica_client.embed_sentence(status.full_text, model="twitter")
            db_tweet.embedding = embeddingdb.session.add(db_tweet)
        db.session.commit()

        #### TODO user_profile info for the return
        return render_template("user_profile.html", user=db_user, tweets=db_user.tweets)
    except Exception as e:
        print(e)
        return jsonify({"message": "OOPS THERE WAS AN ERROR. PLEASE TRY ANOTHER USER."})


@new_routes.route("/reset")
def reset():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "We have successfuly reset the database."})


#
# Classifier Model Prediction
#

@new_routes.route("/predict", methods=["POST"])
def predict():
    ####TODO####
    """ Determines which of two users are more likely to say a given tweet. Assumes users and their tweets have already been stored in the database. Adapted from: https://github.com/LambdaSchool/TwitOff/blob/master/twitoff/predict.py"""

    print("PREDICTION REQUEST...")
    print("FORM DATA:", dict(request.form))
    sn1 = request.form["first_screen_name"]
    sn2 = request.form["second_screen_name"]
    tweet_text = request.form["tweet_text"]

    print("FETCHING TWEETS FROM THE DATABASE...")
    user1 = User.query.filter(User.screen_name == sn1).one()
    user2 = User.query.filter(User.screen_name == sn2).one()

    print("TRAINING THE MODEL...")

    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    print(type(user1_embeddings), user1_embeddings.shape) #> <class 'numpy.ndarray'> (7, 768)
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    print(type(user2_embeddings), user2_embeddings.shape) #> <class 'numpy.ndarray'> (20, 768)
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    #> ValueError: all the input array dimensions for the concatenation axis must match exactly, but along dimension 1,
    # the array at index 0 has size 41 and the array at index 1 has size 768
    #print("EMBEDDINGS", type(embeddings))

    #breakpoint()
    labels = np.concatenate([np.ones(len(user1.tweets)), np.zeros(len(user2.tweets))])
    print("LABELS", type(labels))

    classifier = LogisticRegression().fit(embeddings, labels)

    print("GETTING EMBEDDINGS FOR THE EXAMPLE TEXT...")
    tweet_embedding = basilica_client.embed_sentence(tweet_text, model="twitter")

    print("PREDICTING...")
    results = classifier.predict(np.array(tweet_embedding).reshape(1, -1))
    print(type(results), results.shape) #> <class 'numpy.ndarray'> (7, 768)
    print(results)
    #> [1.] for first user
    #> [0.] for second user

    ####TODO make render template for the results page ####
    return render_template("results.html",
        screen_name1=sn1,
        screen_name2=sn2,
        tweet_text=tweet_text,
        prediction_results=results
    )

