#import modules
from cgitb import enable
from importlib.metadata import MetadataPathFinder
import os
import secrets
from os import path
from flask import Flask, abort, Blueprint, render_template, request, flash, redirect, url_for, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import inspect, create_engine
from sqlalchemy.sql import func, select
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
import datetime



app = Flask(__name__)

app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
views = Blueprint('views', __name__)
mail = Mail(app)

from .models import  User, Files, Survey, Subscription, Questionnaire, Sections, Questions, Dotpoints, Response, Action, Comments, Evidence
from .forms import UploadForm, EditProfileForm
from . import mail

def create_app():
    #app = Flask(__name__)
    
    #directory for sqlite
    basedir = os.path.abspath(os.path.dirname(__file__))

    #initialise database
    # db.init_app(app)

    #secure cookies data
    app.config['SECRET_KEY'] = 'lolo'
    # app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #set up admin
    admin = Admin(app, name='control panel', template_mode='bootstrap3')
    #initialise database
    #db.init_app(app)

    #Create Class controller view  * change this
    class Controller(ModelView):
        def is_accessible(self):
            if current_user.is_admin == True:
                return current_user.is_authenticated
            else:
                return abort(404)
            #return current_user.is_authenticated
        def not_auth(self):
            return "You are not authorised to view this page"

            
    #create admin view
    admin.add_view(Controller(User, db.session))
    
    #Set up loginmanager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    #Import models
    from .models import School

    
    #import routes
    from .views import views
    from .auth import auth

        

    #def create_database(app) 
    #Find string in an array
    engine = create_engine('mysql://ops:ops2022@127.0.0.1/ops')
    insp = inspect(engine)
    table_names = insp.get_table_names()
    if 'subscription' not in table_names:
        db.create_all(app=app)
        in_school = School(school_name = "UniOlly")
        db.session.add(in_school)
        db.session.commit()

        #insert values in table Questionnaire, Sections, Questions, Dotpoints, Response, Action, Comments, Evidence
        #Insert value into table questionnaire
        inquestionnaire  = Questionnaire(name = "Boarding Supervisor Appraisal")
        db.session.add(inquestionnaire)
        db.session.commit()
        #iNSERT VALUES IN TABLE SECTIONS I.E Professional Practice, Supervisor, Team, Administrator
        insections = Sections(title = "Professional Practice", questionnaire_id = 1,  id = 1)
        db.session.add(insections)
        db.session.commit()
        insections2 = Sections(title = "Supervisor Practice", questionnaire_id =1,  id = 2)
        db.session.add(insections2)
        db.session.commit()
        insections3 = Sections(title = "Team Practice", questionnaire_id = 1, id = 3)
        db.session.add(insections3)
        db.session.commit()
        insections4 = Sections(title = "Administrator Practice", questionnaire_id =1,  id = 4)
        db.session.add(insections4)
        db.session.commit()
        #Insert values in table Questions Like 1.1 Aware of and complies with current legislation relevant to the role
        #Insert questions for section 1
        inquestions = Questions(title = "Aware of and complies with current legislation relevant to the role",id =1, section_id = 1, questionnaire_id =1)
        db.session.add(inquestions)
        db.session.commit()
        inquestions2 = Questions(title = "Aware of and complies with organisation requirements", section_id = 1, questionnaire_id =1, id =2)
        db.session.add(inquestions2)
        db.session.commit()
        inquestions3 = Questions(title = "Relevant professional learning completed", section_id = 1, questionnaire_id =1, id =3)
        db.session.add(inquestions3)
        db.session.commit()
        inquestions4 = Questions(title = "Safe Workplace health and safety practices", section_id = 1, questionnaire_id =1, id =4)
        db.session.add(inquestions4)
        db.session.commit()
        #Isert questions for section 2
        inquestions5 = Questions(title = "Contributes to safe activities and environment for all boarders.", section_id = 2, questionnaire_id =1, id =1)
        db.session.add(inquestions5)
        db.session.commit()
        inquestions6 = Questions(title = "Has respectful professional relationships with all boarders.", section_id = 2, questionnaire_id =1, id =2)
        db.session.add(inquestions6)
        db.session.commit()
        inquestions7 = Questions(title = "Supervises boarders effectively, supporting and meeting needs", section_id = 2, questionnaire_id =1, id =3)
        db.session.add(inquestions7)
        db.session.commit()
        inquestions8 = Questions(title = "Facilitates positive boarder behaviours", section_id = 2, questionnaire_id =1, id =4)
        db.session.add(inquestions8)
        db.session.commit()
        inquestions9 = Questions(title = "Provides sensitive appropriate cultural support", section_id = 2, questionnaire_id =1, id =5)
        db.session.add(inquestions9)
        db.session.commit()
        #Insert questions for section 3
        inquestions10 = Questions(title = "Respects and support residence leadership", section_id = 3, questionnaire_id =1, id =1)
        db.session.add(inquestions10)
        db.session.commit()
        inquestions11 = Questions(title = "Has effective respectful relationships with other members of the team", section_id = 3, questionnaire_id =1, id =2)
        db.session.add(inquestions11)
        db.session.commit()
        inquestions12 = Questions(title = "Supports the induction and training of new team members", section_id = 3, questionnaire_id =1, id =3)
        db.session.add(inquestions12)
        db.session.commit()
        #Insert Questions for section 4
        inquestions13 = Questions(title = "Reports and records effectively and as required", section_id = 4, questionnaire_id =1, id =1)
        db.session.add(inquestions13)
        db.session.commit()
        inquestions14 = Questions(title = "Effective parent and school staff relationships", section_id = 4, questionnaire_id =1, id =2)
        db.session.add(inquestions14)
        db.session.commit()
        #Inset values into table dotpoints
        #Insert values in table Dotpoints for all questions
        indotpoints = Dotpoints(sequence_id = 1, question_id =1, questionnaire_id =1, section_id = 1, title = "Has a copy of and complies with job")
        indotpoints = Dotpoints(sequence_id = 2, question_id =1, questionnaire_id =1, section_id = 1, title = "Is also very nice")
        indotpoints = Dotpoints(sequence_id = 3, question_id =1, questionnaire_id =1, section_id = 1, title = "Very helpful too")
        indotpoints = Dotpoints(sequence_id = 4, question_id =1, questionnaire_id =1, section_id = 1, title = "Very helpful too")
        indotpoints = Dotpoints(sequence_id = 5, question_id =1, questionnaire_id =1, section_id = 1, title = "Very helpful too")
        indotpoints = Dotpoints(sequence_id = 6, question_id =1, questionnaire_id =1, section_id = 1, title = "Very helpful too")
        db.session.add(indotpoints)
        db.session.commit()
        indotpoints2 = Dotpoints(sequence_id = 1,question_id =2, questionnaire_id =1, section_id =1, title = "Very good man")
        db.session.add(indotpoints2)
        db.session.commit()
        indotpoints3 = Dotpoints(sequence_id = 1, question_id =  3, questionnaire_id = 1, section_id = 1, title = "Very Good Man" )
        db.session.add(indotpoints3)
        db.session.commit()
        indotpoints4 = Dotpoints(sequence_id = 1, question_id =4, questionnaire_id = 1, section_id =1, title = "Very")
        db.session.add(indotpoints4)
        db.session.commit()
        indotpoints5 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id =1, section_id = 2, title = "Very")
        db.session.add(indotpoints5)
        db.session.commit()
        indotpoints6 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Very")
        db.session.add(indotpoints6)
        db.session.commit()
        indotpoints7 = Dotpoints(sequence_id = 1, question_id = 3, questionnaire_id = 1, section_id =2, title = "Very")
        db.session.add(indotpoints7)
        db.session.commit()
        indotpoints8 = Dotpoints(sequence_id = 1, question_id =4, questionnaire_id = 1, section_id = 2, title = "Very")
        db.session.add(indotpoints8)
        db.session.commit()
        indotpoints9 = Dotpoints(sequence_id = 1, question_id = 5, questionnaire_id =1, section_id =2,  title = "Very")
        db.session.add(indotpoints9)
        db.session.commit()
        indotpoints10 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id = 1, section_id = 3, title = "Very")
        db.session.add(indotpoints10)
        db.session.commit()
        indotpoints11 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Very")
        db.session.add(indotpoints11)
        db.session.commit()
        indotpoints12 = Dotpoints(sequence_id = 1, question_id = 3, questionnaire_id = 1, section_id = 3, title = "Very")
        db.session.add(indotpoints12)
        db.session.commit()
        indotpoints13 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id = 1, section_id = 4, title = "Very")
        db.session.add(indotpoints13)
        db.session.commit()
        indotpoints14 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id = 4, title = "Very")
        db.session.add(indotpoints14)
        db.session.commit()

        # print('Database populated')

        print('Database populated')


    
        #Define expiry date function
        def expiry_date():
            users = User.filter_by(school_id = current_user.school_id)
            now = datetime.datetime.now()
            if now > expiry_date:
                users.is_approved = False
            elif now < expiry_date:
                users.is_approved = True
            



          #if not engine.has_table(engine, 'subscription'):  #to test if a database exists
         #metadata = MetadataPathFinder(engine) 
           #ops.create(engine, checkfirst=True)
           #Table('subscription', metadata)
           #     Column('Id', Integer, primary_key=True, nullable=False),
           #     Column('First Name', varchar, nullable=False),
           #     Column('Last Name', varchar, nullable=False),
           #     Column('EmailID', varchar, nullable=False),
           #     Column('School Name', varchar, nullable=False),
           #     Column('Phone Number', integer, nullable=False)
           #if not database_exists(engine.url):
    #create_database(engine.url)
#else:
    #engine.connect()

    #set up email
    # app.config['MAIL_SERVER']='smtp.gmail.com' #127.0.0.1
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = None
    # app.config['MAIL_PASSWORD'] = None
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = False
    # mail = Mail(app)

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
    mail = Mail(app)

    #initialise database
    # db.init_app(app)

    #blueprint
    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    
    #Create User Loader
    #login_manager = LoginManager()
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

 
