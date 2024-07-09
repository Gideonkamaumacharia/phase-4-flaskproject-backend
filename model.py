from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email= db.Column(db.String)
    password = db.Column(db.String)
    surveys = db.relationship('Survey', back_populates='user')

class Survey(db.Model,SerializerMixin):
    __tablename__='surveys'
    id= db.Column(db.Integer,primary_key=True)
    title= db.Column(db.String)
    description = db.Column(db.String)
    user_id= db.Column(db.Integer,db.ForeignKey('users.id'))
    user= db.relationship('User',back_populates='surveys')
    questions = db.relationship('Qustion',back_populates='survey')

class Question(db.Model,SerializerMixin):
    __tablename__ ='questions'
    id = db.Column(db.Integer, primary_key=True)
    content= db.Column(db.String)
    type= db.Column(db.String)
    survey_id=db.Column(db.Integer,db.ForeignKey('surveys.id'))
    survey = db.relationship('Survey',back_populates='questions')

class Participant(db.Model,SerializerMixin):
    __tablename__ ='participants'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    survey_id= db.Column(db.Integer, db.ForeignKey('surveys.id'))
    completed= db.Column(db.Boolean,default=False)
