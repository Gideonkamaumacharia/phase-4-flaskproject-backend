from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request
from model import db, User


user_fields = {
    'id': fields.Integer,
    'username':fields.String,
    'email': fields.String,
    'password':fields.String
}

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self,user_id=None):
        if user_id:
            user = User.query.get_or_404(user_id)
            return user
        users = User.query.all()
        return users
    
    @marshal_with(user_fields)
    def post(self):
        try:
            data = request.get_json()

            if not all(key in data for key in ('username', 'email', 'password')):
                return {'message': 'Missing required fields'}, 400

            new_user = User(username=data['username'], email=data['email'], password=data['password'])
            new_user.set_password(data['password'])

            db.session.add(new_user)
            db.session.commit()

            return new_user, 201

        except Exception as e:
            print(f"Error in POST request: {str(e)}")
            return {'message': 'Internal Server Error'}, 500

    @marshal_with(user_fields)
    def put(self, user_id):
        try:
            data = request.get_json()
            user = User.query.get_or_404(user_id)

            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.set_password(data['password'])

            db.session.commit()
            return user

        except Exception as e:
            print(f"Error in PUT request: {str(e)}")
            return {'message': 'Internal Server Error'}, 500
    def delete(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return '', 204  
        except Exception as e:
            print(f"Error deleting user: {str(e)}")
            return {'message': 'Failed to delete user'}, 500
    