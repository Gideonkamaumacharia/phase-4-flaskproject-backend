from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    surveys = db.relationship('Survey', back_populates='user')

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, email={self.email}>'

class Survey(db.Model, SerializerMixin):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='surveys')
    questions = db.relationship('Question', back_populates='survey')

    def __repr__(self):
        return f'<Survey id={self.id}, title={self.title}>'

class Question(db.Model, SerializerMixin):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    type = db.Column(db.String)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    survey = db.relationship('Survey', back_populates='questions')

    def __repr__(self):
        return f'<Question id={self.id}, content={self.content}, type={self.type}>'

class Participant(db.Model, SerializerMixin):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'))
    completed = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref='participations')
    survey = db.relationship('Survey', backref='participants')

    def __repr__(self):
        return f'<Participant id={self.id}, user_id={self.user_id}, survey_id={self.survey_id}, completed={self.completed}>'
