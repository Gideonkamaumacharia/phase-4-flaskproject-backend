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

            db.session.add(new_user)
            db.session.commit()

            return new_user, 201

        except Exception as e:
            print(f"Error in POST request: {str(e)}")
            return {'message': 'Internal Server Error'}, 500

    @marshal_with(user_fields)
    def put(self,user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username= data.get('username',user.username)
        user.email=data.get('email',user.email)
        user.password=data.get('password',user.password)
        db.session.commit()
        return user
    def delete(self,user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '',204
    