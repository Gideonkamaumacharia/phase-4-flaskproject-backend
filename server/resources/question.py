from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from model import db, Question, Survey

question_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'type': fields.String,
    'survey_id': fields.Integer
}

class QuestionResource(Resource):
    @marshal_with(question_fields)
    def get(self, question_id=None):
        if question_id:
            question = Question.query.get_or_404(question_id)
            return question
        questions = Question.query.all()
        return questions
    
    @marshal_with(question_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('content', type=str, required=True, help='Content is required')
        parser.add_argument('type', type=str, required=True, choices=('multiple_choice', 'open_ended'), help='Invalid question type')
        parser.add_argument('survey_id', type=int, required=True, help='Survey ID is required')
        data = parser.parse_args()
        
        new_question = Question(content=data['content'], type=data['type'], survey_id=data['survey_id'])
        db.session.add(new_question)
        db.session.commit()
        return new_question, 201
    
    @marshal_with(question_fields)
    def put(self, question_id):
        data = request.get_json()
        question = Question.query.get_or_404(question_id)
        question.content = data.get('content', question.content)
        question.type = data.get('type', question.type)
        question.survey_id = data.get('survey_id', question.survey_id)
        db.session.commit()
        return question
    
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return '', 204
