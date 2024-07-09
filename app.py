from flask import Flask
from flask_migrate import Migrate

from model import db

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

migrate= Migrate(app,db)


if __name__== '__main__':
    app.run(debug=True)