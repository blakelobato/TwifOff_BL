from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    """Gets the user in the database"""
    id = db.Column(db.BigInteger, primary_key=True)
    screen_name = db.Column(db.String(128), nullable=False)
    followers_count = db.Column(db.Integer)
    latest_tweet_id = db.Column(db.BigInteger)

class Tweet(db.Model):
    """class to pull a user's tweets"""
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    full_text = db.Column(db.String(500))
    embedding = db.Column(db.PickleType)

    user = db.relationship("User", backref=db.backref("tweets", lazy=True))

    # def __repr__(self):
    #     return '<User {}>'.format(self.text)
