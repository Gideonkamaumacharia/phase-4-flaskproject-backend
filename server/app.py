from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError 
from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash 
from flask_cors import CORS

from model import db, User
from resources.user import UserResource
from resources.survey import SurveyResource
from resources.question import QuestionResource
from resources.participant import ParticipantResource

import logging


logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '0qwV_Ku1WZjmOKEDZ0OP67MYRQu-VF9-axZXcMH5T58'
CORS(app)

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt()
db.init_app(app)
migrate = Migrate(app, db)
jwt.init_app(app)
bcrypt.init_app(app)
api.init_app(app)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SurveyResource, '/surveys', '/surveys/<int:survey_id>')
api.add_resource(QuestionResource, '/questions', '/questions/<int:question_id>')
api.add_resource(ParticipantResource, '/participants', '/participants/<int:participant_id>')

register_args=reqparse.RequestParser()
register_args.add_argument('username')
register_args.add_argument('email')
register_args.add_argument('password')

class Register(Resource):
    def post(self):
        data = register_args.parse_args()
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(username=data.get('username'),email=data.get('email'),password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message':'New user created successfully'})
    

login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            return jsonify({'message':'User does not exist'})
        if not bcrypt.check_password_hash(user.password,data.get('password')):
            return jsonify({'message':'Password do not match'})
        
        token = create_access_token(identity=user.id)
        return jsonify({'token':token})

api.add_resource(Register,'/register')
api.add_resource(Login,'/login')

if __name__ == '__main__':
    app.run(debug=True)
