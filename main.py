

from flask import Flask, flash, render_template, request, redirect, url_for

# UI/CSS
from flask_bootstrap import Bootstrap

# FORMS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired, URL

from twitter_api import get_tweets
from sentiment_api import get_sentiment

# Database
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime
DEFAULT_DATE = datetime(1900, 1, 1)

import os
DIR = os.path.dirname(os.path.abspath(__file__))
print(DIR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'not-for-prod' #change this before deploying to prod
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DIR + "/HashTags.db"
#Optional: But it will silence the deprecation warning in the console.
db = SQLAlchemy(app)

# create table
class HashTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hashtag = db.Column(db.String(50), unique=True,nullable=False) 
    pos_percent = db.Column(db.String(100), unique=False,nullable=False)    
    neg_percent = db.Column(db.String(100), unique=False,nullable=False)
    mid_percent = db.Column(db.String(100), unique=False,nullable=False)

with app.app_context():
    db.create_all()

class HTForm(FlaskForm):
    hashtag = StringField('hashtag')
    submit = SubmitField("Submit")


sort_id = -1

@app.route("/")
def home():
    global sort_id
    all_hashtags = db.session.query(HashTags).all()

    print(all_hashtags)
    print(type(all_hashtags[0]))

    if sort_id == 0:
        all_hashtags = sorted(all_hashtags,key=lambda x : x.hashtag)
    if sort_id == 1:
        all_hashtags = sorted(all_hashtags,key=lambda x : float(x.pos_percent.replace("%","")), reverse=True)
    if sort_id == 2:
        all_hashtags = sorted(all_hashtags,key=lambda x : float(x.neg_percent.replace("%","")), reverse=True)
    if sort_id == 3:
        all_hashtags = sorted(all_hashtags,key=lambda x : float(x.mid_percent.replace("%","")), reverse=True)

    print(all_hashtags)
    print(type(all_hashtags))
    return render_template('index.html', hashtags=all_hashtags,sort_id=sort_id)


@app.route('/add', methods=["GET", "POST"])
def add():
    form = HTForm()
    print(form.validate_on_submit)
    if form.validate_on_submit():

        # import time
        # time.sleep(10)

        tweets = get_tweets(form.hashtag.data)
        senti = get_sentiment(tweets)

        pos_percent = float(senti['pos_percent'].replace("%",""))
        neg_percent = float(senti['neg_percent'].replace("%",""))
        mid_percent = float(senti['mid_percent'].replace("%",""))

        hashtag = form.hashtag.data
        if hashtag.startswith('#'):
            pass
        else:
            hashtag = '#'+hashtag

        new_ht = HashTags(
            hashtag = hashtag,
            pos_percent = "{:.2f}%".format(pos_percent),
            neg_percent = "{:.2f}%".format(neg_percent),
            mid_percent = "{:.2f}%".format(mid_percent)

        )
        db.session.add(new_ht)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html',form=form)

@app.route('/sort/<int:id>', methods=["GET", "POST"])
def sort(id):
    global sort_id
    sort_id = id
    return redirect(url_for('home'))

@app.route('/refresh/<int:id>', methods=["GET", "POST"])
def refresh(id):
    print('refresh',id)
    ht = HashTags.query.get(id)

    tweets = get_tweets(ht.hashtag)
    senti = get_sentiment(tweets)

    ht.pos_percent = "{:.2f}%".format(float(senti['pos_percent'].replace("%","")))
    ht.neg_percent = "{:.2f}%".format(float(senti['neg_percent'].replace("%","")))
    ht.mid_percent = "{:.2f}%".format(float(senti['mid_percent'].replace("%","")))

    db.session.commit()

    return redirect(url_for('home'))



@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    try:
        print(id)
        ht = HashTags.query.get(id)
        db.session.delete(ht)
        db.session.commit()
    except:
        print('error: id: ', str(id) ,' not deleted')
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.static_folder = 'static'
    app.debug = True
    app.run()