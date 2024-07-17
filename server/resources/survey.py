from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with, reqparse
from model import db, Survey, User, Question

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}

question_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'type': fields.String,
}

survey_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'user': fields.Nested(user_fields),
    'questions': fields.List(fields.Nested(question_fields)),
}


class SurveyResource(Resource):
    @marshal_with(survey_fields)
    def get(self, survey_id=None):
        if survey_id:
            return Survey.query.get_or_404(survey_id)
        return Survey.query.all()

    @marshal_with(survey_fields)
    def post(self):
        try:
            data = request.get_json()

            # Extract user data
            user_data = data.get('user')
            if not user_data:
                return {'message': 'User data is required'}, 400

            user_id = user_data.get('id')
            if not user_id:
                return {'message': 'User ID is required'}, 400

            # Retrieve the user from the database
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404

            # Extract questions data
            questions_data = data.get('questions', [])
            if not questions_data:
                return {'message': 'At least one question is required'}, 400

            # Create Question objects
            questions = []
            for question_data in questions_data:
                question = Question(
                    content=question_data.get('content'),
                    type=question_data.get('type'),
                )
                questions.append(question)

            # Create Survey object and associate with user and questions
            new_survey = Survey(
                title=data.get('title'),
                description=data.get('description'),
                user=user,
                questions=questions
            )

            # Add new survey to the database session and commit
            db.session.add(new_survey)
            db.session.commit()

            # Construct JSON response
            response_data = {
                'id': new_survey.id,
                'title': new_survey.title,
                'description': new_survey.description,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'questions': [
                    {
                        'id': question.id,
                        'content': question.content,
                        'type': question.type,
                    } for question in questions
                ]
            }

            return jsonify(response_data), 201

        except Exception as e:
            print(f"Error in POST request: {str(e)}")
            return {'message': 'Internal Server Error'}, 500

    @marshal_with(survey_fields)
    def put(self, survey_id):
        try:
            data = request.get_json()
            survey = Survey.query.get_or_404(survey_id)
            survey.title = data.get('title', survey.title)
            survey.description = data.get('description', survey.description)
            db.session.commit()
            return survey
        except Exception as e:
            print(f"Error in PUT request: {str(e)}")
            return {'message': 'Internal Server Error'}, 500

    def delete(self, survey_id):
        try:
            survey = Survey.query.get_or_404(survey_id)
            db.session.delete(survey)
            db.session.commit()
            return {'message': 'Survey deleted successfully'}, 204
        except Exception as e:
            print(f"Error deleting survey: {str(e)}")
            return {'message': 'Failed to delete survey'}, 500
