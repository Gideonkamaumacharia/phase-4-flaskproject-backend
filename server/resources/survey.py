from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
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
    def get(self,survey_id=None):
        if survey_id:
            survey = Survey.query.get_or_404(survey_id)
            return survey
        surveys = Survey.query.all()
        return surveys
    
    @marshal_with(survey_fields)
    def post(self):
        data = request.get_json()
        new_survey = Survey(title=data['title'],description=data['description'])
        db.session.add(new_survey)
        db.session.commit()
        return new_survey,201
    @marshal_with(survey_fields)
    def put(self,survey_id):
        data = request.get_json()
        survey = Survey.query.get_or_404(survey_id)
        survey.title= data.get('title',survey.title)
        survey.description=data.get('description',survey.description)
        db.session.commit()
        return survey
    
    def delete(self,survey_id):
        survey = Survey.query.get_or_404(survey_id)
        db.session.delete(survey)
        db.session.commit()
        return '',204
    