#import modules
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint, Column, String, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#import modules db
from . import db, app

#Set up login managers
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Define school table
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    school_name = db.Column(db.String(255))
    user = db.relationship('User', backref='school', lazy=True)

   
#define User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    #survey = db.relationship('Survey', backref='author', lazy=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"

#Define Manager table with school as foreign key
class Manager(db.Model):
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employee_id =  db.Column(db.Integer, db.ForeignKey('user.id'))

    __table_args__ = (db.PrimaryKeyConstraint('manager_id','employee_id'),)

#Define Subsciption table
class Subscription(db.Model):
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False, primary_key = True)
    expiry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


#Define survey table * Remember to remove this
class Survey(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    title = db.Column(db.String(100))
    document_file = db.Column(db.String(255))

    #Foreign constraint of user id and manager id in the user table
    ForeignKeyConstraint( ['user_id', 'manager_id'], ['user.id', 'user.manager_id'] )

    def __repr__(self):
        return f"Survey('{self.title}', '{self.date_posted}')"

    
#define Questionnaire table
class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    survey_id = db.Column(db.Integer)
    #foreign key constraint for user id and survey id in survey table
    ForeignKeyConstraint( ['user_id', 'survey_id'], ['survey.user_id', 'survey.id'] )

    def __repr__(self):
        return f"Questionnaire('{self.name}')"


    
        
#define survey sections
class Sections(db.Model):
    id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    title = db.Column(db.String(100)) #Varchar

   
    #make questionnaire and section id  composite primary key
    __table_args__ = (db.PrimaryKeyConstraint('id', 'questionnaire_id'),)


    def __repr__(self):
        return f'<SurveySections "{self.title}">'

#define survey questions 
class Questions(db.Model):
    id = db.Column(db.Integer)
    title = db.Column(db.String(100))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

    #make section number and questionnaire number and question number composite primary key
    __table_args__ = (db.PrimaryKeyConstraint('id', 'section_id', 'questionnaire_id'),db.ForeignKeyConstraint(['questionnaire_id', 'section_id'], ['sections.questionnaire_id', 'sections.id']) )

    def __repr__(self):
        return f'<SurveyQuestions "{self.title}">'


#Dotpoints
#define dotpoints table with foreign key constraint of questionnaire, question and section and primary key constraint of questionnaire, question, section and sequence
class Dotpoints(db.Model):
    sequence_id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    title = db.Column(db.String(500))

   #make questionnaire, question, section, sequence - primary key constraint
    __table_args__ = (db.PrimaryKeyConstraint('sequence_id', 'questionnaire_id', 'section_id', 'question_id'), db.ForeignKeyConstraint(['questionnaire_id', 'section_id', 'question_id'], ['questions.questionnaire_id', 'questions.section_id', 'questions.id']),)

    
    def __repr__(self):
        return f'<SurveyDotpoints "{self.title}">'

#Define response table with foreign key constraint of questionnaire, question, section and dotpoint and primary key constraint of questionnaire, question, section, dotpoint and sequence
class Response(db.Model):
    # id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_posted =  db.Column(db.Date, default = func.current_date())
    rating = db.Column(db.String(100))
   
    #make questionnaire, question, section,  sequence   - primary key constraint and foreign key constraint
    __table_args__ = (db.PrimaryKeyConstraint( 'questionnaire_id', 'section_id', 'question_id', 'user_id', 'date_posted'), db.ForeignKeyConstraint(['questionnaire_id', 'section_id', 'question_id'], ['questions.questionnaire_id', 'questions.section_id', 'questions.id']),
   ForeignKeyConstraint(['user_id'], ['user.id'] ) )

    
    def __repr__(self):
        return f'<SurveyChoices "{self.rating}">'

    #Define action table with foreign key constraint of questionnaire, question, section and dotpoint and primary key constraint of questionnaire, question, section, dotpoint and sequence
class Action(db.Model):
    # id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_posted = db.Column(db.Date, default = func.current_date())
    title = db.Column(db.String(100))
    
   
    #make questionnaire, question, section,  sequence   - primary key constraint
    __table_args__ = (db.PrimaryKeyConstraint( 'questionnaire_id', 'section_id', 'question_id', 'date_posted', 'user_id' ), db.ForeignKeyConstraint(['questionnaire_id', 'section_id', 'question_id'], ['questions.questionnaire_id', 'questions.section_id', 'questions.id']),
    ForeignKeyConstraint(['user_id'], ['user.id'] ))

    def __repr__(self):
        return f'<SurveyChoices "{self.title}">'


   #Make comments table with foreign key constraint of questionnaire, question, section and dotpoint and primary key constraint of questionnaire, question, section, dotpoint and sequence
class Comments(db.Model):
    # id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(500))
    date_posted = db.Column(db.Date, default = func.current_date() )
    
   
    #make questionnaire, question, section,  sequence   - primary key constraint
    __table_args__ = (db.PrimaryKeyConstraint( 'questionnaire_id', 'section_id', 'question_id', 'date_posted', 'user_id'), db.ForeignKeyConstraint(['questionnaire_id', 'section_id', 'question_id'], ['questions.questionnaire_id', 'questions.section_id', 'questions.id']),
    ForeignKeyConstraint(['user_id'], ['user.id'] ))

    def __repr__(self):
        return f'<SurveyChoices "{self.title}">'
    
    #Make evidence table with foreign key constraint of questionnaire, question, section and dotpoint and primary key constraint of questionnaire, question, section, dotpoint and sequence
class Evidence(db.Model):
    # id = db.Column(db.Integer)
    questionnaire_id = db.Column(db.Integer)
    section_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    date_posted = db.Column(db.Date, default = func.current_date())
    title = db.Column(db.String(100))
   
    #make questionnaire, question, section,  sequence   - primary key constraint
    __table_args__ = (db.PrimaryKeyConstraint( 'questionnaire_id', 'section_id', 'question_id', 'date_posted', 'user_id'), db.ForeignKeyConstraint(['questionnaire_id', 'section_id', 'question_id'], ['questions.questionnaire_id', 'questions.section_id', 'questions.id']),
    ForeignKeyConstraint(['user_id'], ['user.id'] ))

    def __repr__(self):
        return f'<SurveyChoices "{self.title}">'
    



























#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100))
#     questionnaire_id = db.Column(db.Integer)
#     section_id = db.Column(db.Integer)
#     question_id = db.Column(db.Integer)
#     choices = db.Column(db.String(255))
#     comments = db.Column(db.String(255))
#     evidence = db.Column(db.String(255))
#     actions = db.Column(db.String(255))
#     choices2 = db.Column(db.String(255))
#     comments2 = db.Column(db.String(255))
#     evidence2 = db.Column(db.String(255))
#     actions2 = db.Column(db.String(255))
#     choices3 = db.Column(db.String(255))
#     comments3 = db.Column(db.String(255))
#     evidence3 = db.Column(db.String(255))
#     actions3 = db.Column(db.String(255))
#     choices4 = db.Column(db.String(255))
#     comments4 = db.Column(db.String(255))
#     evidence4 = db.Column(db.String(255))
#     actions4 = db.Column(db.String(255))
#     ForeignKeyConstraint(
#                 ['questionnaire_id', 'section_id', 'question_id'],
#                 ['questionnaire.id', 'sections.id', 'questions.id'],
#                 onupdate="CASCADE", ondelete="SET NULL"
#     )
#     def __repr__(self):
#         return f'<SurveySubQuestions "{self.text}">'


# # #define survey sub-questions3
# class SubQuestions3(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100))
#     questionnaire_id = db.Column(db.Integer)
#     section_id = db.Column(db.Integer)
#     question_id = db.Column(db.Integer)
#     choices = db.Column(db.String(255))
#     comments = db.Column(db.String(255))
#     evidence = db.Column(db.String(255))
#     actions = db.Column(db.String(255))
#     choices2 = db.Column(db.String(255))
#     comments2 = db.Column(db.String(255))
#     evidence2 = db.Column(db.String(255))
#     actions2 = db.Column(db.String(255))
#     choices3 = db.Column(db.String(255))
#     comments3 = db.Column(db.String(255))
#     evidence3 = db.Column(db.String(255))
#     actions3 = db.Column(db.String(255))
#     ForeignKeyConstraint(
#                 ['questionnaire_id', 'section_id', 'question_id'],
#                 ['questionnaire.id', 'sections.id', 'questions.id'],
#                 onupdate="CASCADE", ondelete="SET NULL"
#     )
#     def __repr__(self):
#         return f'<SurveySubQuestions "{self.text}">'

# # #define survey sub-questions4
# class SubQuestions4(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100))
#     questionnaire_id = db.Column(db.Integer)
#     section_id = db.Column(db.Integer)
#     question_id = db.Column(db.Integer)
#     choices = db.Column(db.String(255))
#     comments = db.Column(db.String(255))
#     evidence = db.Column(db.String(255))
#     actions = db.Column(db.String(255))
#     choices2 = db.Column(db.String(255))
#     comments2 = db.Column(db.String(255))
#     evidence2 = db.Column(db.String(255))
#     actions2 = db.Column(db.String(255))
#     ForeignKeyConstraint(
#                 ['questionnaire_id', 'section_id', 'question_id'],
#                 ['questionnaire.id', 'sections.id', 'questions.id'],
#                 onupdate="CASCADE", ondelete="SET NULL"
#     )
#     def __repr__(self):
#         return f'<SurveySubQuestions "{self.text}">'


#define Files Tables
class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    file = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer)
    review_id = db.Column(db.Integer)
    ForeignKeyConstraint(
                ['user_id', 'review_id'],
                ['user.id', 'reviews.id'],
    )
    def __repr__(self):
        return f'<Files "{self.filename}">'

# Define datefield table * (For reminders) Change this one
class DateField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer)
    review_id = db.Column(db.Integer)
    ForeignKeyConstraint(
                ['user_id', 'review_id'],
                ['user.id', 'reviews.id'],
    )
    def __repr__(self):
        return f'<DateField "{self.date}">'