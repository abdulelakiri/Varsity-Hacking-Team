from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'k\xbf\xd6Y|\x1f\xf4Q\x0eQ\x0e\xf2\x80h'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'

db = SQLAlchemy(app)


from webpage.routes import home, page_not_found

app.register_blueprint(home)
app.register_error_handler(404, page_not_found)

class Incoming_tweets(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(300))
    time_tweeted = db.Column(db.String(50))
    location = db.Column(db.String(50))
    category = db.Column(db.String(50))
    realness = db.Column(db.Boolean)
    confidence = db.Column(db.Float(10))

    Pending_tweets = db.relationship(
        'Pending_tweets', backref='pending_tweets', lazy='dynamic')

    def __repr__(self):
        dictionary = {
            "id": self.id,
            "tweet": self.tweet,
            "time_tweeted": self.time_tweeted,
            "location": self.location,
            "category": self.category,
            "realness": self.Realness,
            "confidence": self.confidence
        }
        return json.dumps(dictionary)
    
class Pending_tweets(db.Model):
    tweet_id = db.Column(db.ForeignKey(Incoming_tweets.id), primary_key=True)

    def __repr__(self):
        dictionary = {
            "request_id": self.request_id,
        }
        return json.dumps(dictionary)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port='8080',debug=True)