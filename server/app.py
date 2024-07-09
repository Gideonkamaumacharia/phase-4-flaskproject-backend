from flask import Flask
from flask_migrate import Migrate

from server.model import db,User,Survey,Question,Participant

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

migrate= Migrate(app,db)


if __name__== '__main__':
    app.run(debug=True)