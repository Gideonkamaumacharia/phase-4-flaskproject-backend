from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from model import db, User, Survey, Question, Participant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with your secret key
app.config['BCRYPT_LOG_ROUNDS'] = 12  # Adjust as per your application needs

# Initialize Flask extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# Define your seeding functions
def create_users():
    """
    Create sample users and commit to the database.
    """
    try:
        user1 = User(username='john_doe', email='john.doe@example.com', password=bcrypt.generate_password_hash('password1').decode('utf-8'))
        user2 = User(username='jane_smith', email='jane.smith@example.com', password=bcrypt.generate_password_hash('password2').decode('utf-8'))
        
        db.session.add_all([user1, user2])
        db.session.commit()
        print("Users created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating users: {str(e)}")

def create_surveys():
    """
    Create sample surveys and commit to the database.
    """
    try:
        user1 = User.query.filter_by(username='john_doe').first()
        user2 = User.query.filter_by(username='jane_smith').first()
        
        survey1 = Survey(title='Survey 1', description='Description of Survey 1', user=user1)
        survey2 = Survey(title='Survey 2', description='Description of Survey 2', user=user2)
        
        db.session.add_all([survey1, survey2])
        db.session.commit()
        print("Surveys created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating surveys: {str(e)}")

def create_questions():
    """
    Create sample questions and commit to the database.
    """
    try:
        survey1 = Survey.query.filter_by(title='Survey 1').first()
        survey2 = Survey.query.filter_by(title='Survey 2').first()
        
        question1 = Question(content='Question 1 content', type='multiple_choice', survey=survey1)
        question2 = Question(content='Question 2 content', type='open_ended', survey=survey1)
        question3 = Question(content='Question 3 content', type='multiple_choice', survey=survey2)
        
        db.session.add_all([question1, question2, question3])
        db.session.commit()
        print("Questions created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating questions: {str(e)}")

def create_participants():
    """
    Create sample participants and commit to the database.
    """
    try:
        user1 = User.query.filter_by(username='john_doe').first()
        user2 = User.query.filter_by(username='jane_smith').first()
        survey1 = Survey.query.filter_by(title='Survey 1').first()
        survey2 = Survey.query.filter_by(title='Survey 2').first()
        
        participant1 = Participant(user=user1, survey=survey1, completed=True)
        participant2 = Participant(user=user2, survey=survey2, completed=False)
        
        db.session.add_all([participant1, participant2])
        db.session.commit()
        print("Participants created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating participants: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        create_users()
        create_surveys()
        create_questions()
        create_participants()
