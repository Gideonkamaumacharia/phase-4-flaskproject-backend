from model import db, bcrypt ,User, Survey, Question, Participant 


def create_users():
    
    user1 = User(username='john_doe', email='john.doe@example.com', password='password1')
    user2 = User(username='jane_smith', email='jane.smith@example.com', password='password2')
    
    
    db.session.add_all([user1, user2])
    db.session.commit()

def create_surveys():
    
    user1 = User.query.filter_by(username='john_doe').first()
    user2 = User.query.filter_by(username='jane_smith').first()
    
    
    survey1 = Survey(title='Survey 1', description='Description of Survey 1', user=user1)
    survey2 = Survey(title='Survey 2', description='Description of Survey 2', user=user2)
    
 
    db.session.add_all([survey1, survey2])
    db.session.commit()

def create_questions():

    survey1 = Survey.query.filter_by(title='Survey 1').first()
    survey2 = Survey.query.filter_by(title='Survey 2').first()
    
   
    question1 = Question(content='Question 1 content', type='multiple_choice', survey=survey1)
    question2 = Question(content='Question 2 content', type='open_ended', survey=survey1)
    question3 = Question(content='Question 3 content', type='multiple_choice', survey=survey2)
    
    
    db.session.add_all([question1, question2, question3])
    db.session.commit()

def create_participants():

    user1 = User.query.filter_by(username='john_doe').first()
    user2 = User.query.filter_by(username='jane_smith').first()
    survey1 = Survey.query.filter_by(title='Survey 1').first()
    survey2 = Survey.query.filter_by(title='Survey 2').first()
    

    participant1 = Participant(user=user1, survey=survey1, completed=True)
    participant2 = Participant(user=user2, survey=survey2, completed=False)

    db.session.add_all([participant1, participant2])
    db.session.commit()


