from flask import Flask,jsonify,request
from flask_migrate import Migrate
from flask_restful import Api,Resource,fields,marshal_with

from model import db,User,Survey,Question,Participant

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db.init_app(app)

migrate= Migrate(app,db)
api =Api(app)

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
        data = request.get_json()
        new_user = User(username=data['username'],email=data['email'],password=data['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user,201
    @marshal_with(user_fields)
    def put(self,user_id):
        data = request.get_json()
        user = User.query.get_or_404(user_id)
        user.username= data.get('username',user.username)
        user.email=data.get('email',user.email)
        user.password=data.get('password',user.password)
        db.session.commit()
        return user
@app.route('/users',methods= ['GET'])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify({'message':'User not found!'}),404
    return jsonify([{'id':user.id,'username':user.username,'email':user.email,'password':user.password}for user in users]),200
@app.route('/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message':'User not found'}),404
    return jsonify({'id':user.id,'username':user.username,'email':user.email,'password':user.password}),200
@app.route('/users' ,methods = ['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'],email=data['email'],password=data['password'])
    db.session.add(new_user)
    db.sesssion.commit()
    return jsonify({'message':'user added successfully'}),200
@app.route('users/<int:id>',methods= ['PUT'])
def update_users(id):
    data= request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message':'User not found'}),404
    user.username= data['username']
    user.email= data['email']
    user.password= data['password']
    db.session.commit()
    return jsonify({'message':'User added successfully.'}),200
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': f'User {id} does not exist '}),404
    db.session.delete(user)
    db.session.commmit()
    
if __name__== '__main__':
    app.run(debug=True)