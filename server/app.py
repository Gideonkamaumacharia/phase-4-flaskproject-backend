from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError  # Import IntegrityError from SQLAlchemy

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

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SurveyResource, '/surveys', '/surveys/<int:survey_id>')
api.add_resource(QuestionResource, '/questions', '/questions/<int:question_id>')
api.add_resource(ParticipantResource, '/participants', '/participants/<int:participant_id>')

@app.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, help='Email address is required', required=True)
    parser.add_argument('password', type=str, help='Password is required', required=True)
    data = parser.parse_args()

    try:
        user = User.query.filter_by(email=data['email']).first()
        logging.debug(f"User found: {user}")

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

    except IntegrityError:
        db.session.rollback()
        return {'message': 'Email address already registered'}, 409

    except Exception as e:
        logging.error(f"Error in login: {e}")
        db.session.rollback()
        return {'message': 'Internal Server Error'}, 500
if __name__ == '__main__':
    app.run(debug=True)
