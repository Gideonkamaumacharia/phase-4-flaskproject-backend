from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from model import db
from resources.user import UserResource
from resources.survey import SurveyResource
from resources.question import QuestionResource
from resources.participant import ParticipantResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate = Migrate(app,db)
api = Api(app)


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(SurveyResource, '/surveys', '/surveys/<int:survey_id>')
api.add_resource(QuestionResource, '/questions', '/questions/<int:question_id>')
api.add_resource(ParticipantResource, '/participants', '/participants/<int:participant_id>')

if __name__ == '__main__':
    app.run(debug=True)
