from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError  
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

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SurveyResource, '/surveys', '/surveys/<int:survey_id>')
api.add_resource(QuestionResource, '/questions', '/questions/<int:question_id>')
api.add_resource(ParticipantResource, '/participants', '/participants/<int:participant_id>')


@app.route('/signup', methods=['POST'])
def signup():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='Username is required', required=True)
    parser.add_argument('email', type=str, help='Email address is required', required=True)
    parser.add_argument('password', type=str, help='Password is required', required=True)
    data = parser.parse_args()

    try:
        # Check if the email is already registered
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email address already registered'}, 409

        # Create a new user
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        # Return the newly created user data
        return {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}, 201

    except Exception as e:
        logging.error(f"Error in sign up: {e}")
        db.session.rollback()
        return {'message': 'Internal Server Error'}, 500

# Login endpoint to authenticate users and issue JWT tokens
@app.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='Email address is required', required=True)
    parser.add_argument('password', type=str, help='Password is required', required=True)
    data = parser.parse_args()

    try:
        user = User.query.filter_by(email=data['email']).first()

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

    except Exception as e:
        logging.error(f"Error in login: {e}")
        return {'message': 'Internal Server Error'}, 500

# Resource classes (UserResource, SurveyResource, QuestionResource, ParticipantResource) and their routes (already provided in your code)

if __name__ == '__main__':
    app.run(debug=True)
