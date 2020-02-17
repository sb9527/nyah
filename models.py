import os, sys
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask import abort

database_path = os.environ['DATABASE_URL']

db=SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"]=database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app=app
    db.init_app(app)

class Data_Population:
    def insert(self, *args):
        error = False
        formated = None
        try:
            db.session.add(self)

            for child in args:
                db.session.add(child)

            db.session.commit()

            formated = self.format()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()  

        if error:
            abort(400) 

        return formated

    def update(self):
        error = False
        formated = None
        try:
            db.session.commit()

            formated = self.format()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()  

        if error:
            abort(400)  

        return formated

    def delete(self):
        error = False
        deleted = None
        try:
            db.session.delete(self)

            deleted = self.id

            db.session.commit()
        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()  

        if error:
            abort(400)  

        return deleted


class User(db.Model, Data_Population):
    __tablename__='users'

    id=db.Column(Integer, primary_key=True)
    
    auth0_user_id = db.Column(String, nullable=False, unique=True)
    nickname = db.Column(String(12), nullable=False)
    picture_url = db.Column(String, nullable=False)

    create_time=db.Column(DateTime, default=datetime.now())

    voices = db.relationship('Voice', cascade="all,delete", backref='parent_user', lazy=True) 
    likes = db.relationship('Like', cascade="all,delete", backref='parent_user', lazy=True)      

    def format(self):
        return {
            'id':self.id,
            'auth0_user_id':self.auth0_user_id,
            'nickname':self.nickname,
            'picture_url':self.picture_url
        }


class Voice(db.Model, Data_Population):
    __tablename__='voices'

    id=db.Column(Integer, primary_key=True)
    text=db.Column(String(120))
    author_id=db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    replying_to=db.Column(Integer, db.ForeignKey('voices.id'), nullable=True)

    create_time=db.Column(DateTime, default=datetime.now())

    pictures = db.relationship('Picture', cascade="all,delete", backref='parent_voice', lazy=True)
    likes = db.relationship('Like', cascade="all,delete", backref='parent_voice', lazy=True)
    replies = db.relationship('Voice', remote_side=[replying_to], lazy=True)

    def format(self):
        return {
            'id':self.id,
            'text':self.text,
            'create_time':self.create_time.timestamp(),
            'author':{
                'id':self.author_id,
                'nickname':self.parent_user.nickname,
                'picture_url':self.parent_user.picture_url
            },
            'replying_to':self.replying_to,
            'pictures':list(picture.url for picture in self.pictures),
            'likes':list(like.user_id for like in self.likes),
            'replies':list(voice.id for voice in self.replies)
        }


class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(Integer, primary_key=True)
    url = db.Column(String)
    voice_id = db.Column(Integer, db.ForeignKey('voices.id'))


class Like(db.Model, Data_Population):
    __tablename__ = 'likes'

    id = db.Column(Integer, primary_key=True)
    like = db.Column(Boolean)
    voice_id = db.Column(Integer, db.ForeignKey('voices.id'))
    user_id = db.Column(Integer, db.ForeignKey('users.id')) 

    def format(self):
        return {
            'like':self.like
        }   