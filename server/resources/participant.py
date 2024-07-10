from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from model import db, Participant, User, Survey

participant_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'survey_id': fields.Integer,
    'completed': fields.Boolean
}

class ParticipantResource(Resource):
    @marshal_with(participant_fields)
    def get(self, participant_id=None):
        if participant_id:
            participant = Participant.query.get_or_404(participant_id)
            return participant
        participants = Participant.query.all()
        return participants
    
    @marshal_with(participant_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID is required')
        parser.add_argument('survey_id', type=int, required=True, help='Survey ID is required')
        parser.add_argument('completed', type=bool, required=False, default=False)
        data = parser.parse_args()
        
        new_participant = Participant(user_id=data['user_id'], survey_id=data['survey_id'], completed=data['completed'])
        db.session.add(new_participant)
        db.session.commit()
        return new_participant, 201
    
    @marshal_with(participant_fields)
    def put(self, participant_id):
        data = request.get_json()
        participant = Participant.query.get_or_404(participant_id)
        participant.user_id = data.get('user_id', participant.user_id)
        participant.survey_id = data.get('survey_id', participant.survey_id)
        participant.completed = data.get('completed', participant.completed)
        db.session.commit()
        return participant
    
    def delete(self, participant_id):
        participant = Participant.query.get_or_404(participant_id)
        db.session.delete(participant)
        db.session.commit()
        return '', 204
