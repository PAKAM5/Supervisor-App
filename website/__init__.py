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
from flask_mail import Mail, Message
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
        #1.1
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 1, title = "Understands and complies with the Commonwealth and State laws that affect their role and knows how to recognise and respond to breaches of these laws.")
        db.session.add(indotpoints)
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 2, title = "Is aware of the child protection and mandatory reporting laws of their State or Territory and responds appropriately when a concern about the safety of a young person is raised.")
        db.session.add(indotpoints)
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 3, title = "Understands the indicators of abuse and what forms a reasonable belief about abuse.")
        db.session.add(indotpoints)
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 4, title = "Completes all mandatory reporting requirements,including written reports.")
        db.session.add(indotpoints)
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 5, title = "Acts appropriately in all their dealings with young people.")
        db.session.add(indotpoints)
        indotpoints = Dotpoints(questionnaire_id =1, section_id = 1, question_id =1, sequence_id = 6, title = "Follows anethical process in reporting any breaches of the law or code of conduct by others.")
        db.session.add(indotpoints)
        db.session.commit()
        #1.2
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 1, title = "Has a copy of and complies with job description documents.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 2, title = "Knows and actively supports the organisation vision, mission and objectives.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 3, title = "Is familiar with and complies with residence policies and procedures")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 4, title = "Has a copy of and complies with the residence Code of Conduct.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 5, title = "Has a copy of the residence social media and IT policies and models responsible use of technology.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 6, title = "Has a copy of and complies with the residence privacy policy and procedures.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 7, title = "Understands and maintains professional relationships.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 8, title = "Understands professional boundaries with students and observes in all practice.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 9, title = "Models positive responsible behaviour and positive standards in dress and appearance.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 10, title = "Complies with Management in structions and expectations conveyed.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 11, title = "Models punctuality for duties and meetings.")
        db.session.add(indotpoints2)
        indotpoints2 = Dotpoints(questionnaire_id =1, section_id =1, question_id =2, sequence_id = 12, title = "Is familiar with and complies with the staff grievance procedure.")
        db.session.add(indotpoints2)
        db.session.commit()
        #1.3
        indotpoints3 = Dotpoints(sequence_id = 1, question_id =  3, questionnaire_id = 1, section_id = 1, title = "Has a personal professional development plan, and attends all professional development as required." )
        db.session.add(indotpoints3)
        indotpoints3 = Dotpoints(sequence_id = 2, question_id =  3, questionnaire_id = 1, section_id = 1, title = "Is current and up to date with required clearances, licences and qualifications, that may include: First Aid (HLTAID003), Safe Working with Children clearance, bus licence, Duty of Care, Boarding Fundamentals, Certificate IV in Community Services - Student Residential Care(CHC42015).")
        db.session.add(indotpoints3)
        indotpoints3 = Dotpoints(sequence_id = 3, question_id =  3, questionnaire_id = 1, section_id = 1, title = "Seeks help and support when needed from Head of Boarding/Manager or colleagues." )
        db.session.add(indotpoints3)
        indotpoints3 = Dotpoints(sequence_id = 4, question_id =  3, questionnaire_id = 1, section_id = 1, title = "Seeks feedback to improve their practice." )
        db.session.add(indotpoints3)
        db.session.commit()
        #1.4
        indotpoints4 = Dotpoints(sequence_id = 1, question_id =4, questionnaire_id = 1, section_id =1, title = "Has knowledge of the residence Work place Health and Safety policy and is consistent in safe work practices")
        db.session.add(indotpoints4)
        indotpoints4 = Dotpoints(sequence_id = 2, question_id =4, questionnaire_id = 1, section_id =1, title = "Has knowledge of the procedures for, and practices hazard identification, management and reporting.")
        db.session.add(indotpoints4)
        indotpoints4 = Dotpoints(sequence_id = 3, question_id =4, questionnaire_id = 1, section_id =1, title = "Responds correctly and consistently to emergencies, following Residence procedures.")
        db.session.add(indotpoints4)
        indotpoints4 = Dotpoints(sequence_id = 4, question_id =4, questionnaire_id = 1, section_id =1, title = "Participates in regular emergency drills and complies with recording/reporting requirements.")
        db.session.add(indotpoints4)
        indotpoints4 = Dotpoints(sequence_id = 5, question_id =4, questionnaire_id = 1, section_id =1, title = "Knows how to undertake Risk Assessment and Management, as required.")
        db.session.add(indotpoints4)
        db.session.commit()
        #2.1
        indotpoints5 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id =1, section_id = 2, title = "Understands the concepts of ‘duty of care’, ‘non-delegable duty of care’ and ‘contributory negligence’.")
        db.session.add(indotpoints5) 
        indotpoints5 = Dotpoints(sequence_id = 2, question_id = 1, questionnaire_id =1, section_id = 2, title = "Ensures that personal practice, and the residence environment and activities always provide a high standard of safety for students.")
        db.session.add(indotpoints5)
        indotpoints5 = Dotpoints(sequence_id = 3, question_id = 1, questionnaire_id =1, section_id = 2, title = "Knows emergency responses to student health issues, including anaphylactic shock and suicidal ideation.")
        db.session.add(indotpoints5)
        indotpoints5 = Dotpoints(sequence_id = 4, question_id = 1, questionnaire_id =1, section_id = 2, title = "Conforms to the Residence procedures for safe administration of medication")
        db.session.add(indotpoints5)
        db.session.commit()
        #2.2
        indotpoints6 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Has positive, respectful professional relationships with all students.")
        db.session.add(indotpoints6)
        indotpoints6 = Dotpoints(sequence_id = 2, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Has nurturing, caring relationships with students, exhibiting empathy and patience.")
        db.session.add(indotpoints6)
        indotpoints6 = Dotpoints(sequence_id = 3, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Reacts and responds to students professionally, with positive, respectful communication with students.")
        db.session.add(indotpoints6)
        indotpoints6 = Dotpoints(sequence_id = 4, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Implements and manages consistent, appropriate routines in the Residence.")
        db.session.add(indotpoints6)
        indotpoints6 = Dotpoints(sequence_id = 5, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Empowers students to becoming self-managing.")
        db.session.add(indotpoints6)
        indotpoints6 = Dotpoints(sequence_id = 6, question_id = 2, questionnaire_id = 1, section_id =2 ,title = "Manages student or parent complaints appropriately and effectively.")
        db.session.add(indotpoints6)
        db.session.commit()
        #2.3
        indotpoints7 = Dotpoints(sequence_id = 1, question_id = 3, questionnaire_id = 1, section_id =2, title = "Supervises students effectively and actively, being involved and where the students are.")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 2, question_id = 3, questionnaire_id = 1, section_id =2, title = "Actively monitors student behaviour and needs and intervenes effectively when required.")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 3, question_id = 3, questionnaire_id = 1, section_id =2, title = "Actively contributes to students’ well-being by supporting and meeting needs.")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 4, question_id = 3, questionnaire_id = 1, section_id =2, title = "Actively encourages and assists students to maintain their required homework and study routines")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 5, question_id = 3, questionnaire_id = 1, section_id =2, title = "Provides interesting, engaging activities, as required.")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 6, question_id = 3, questionnaire_id = 1, section_id =2, title = "Contributes to residence student development plan and activities.")
        db.session.add(indotpoints7)
        indotpoints7 = Dotpoints(sequence_id = 7, question_id = 3, questionnaire_id = 1, section_id =2, title = "Reads and responds appropriately to staff daily log/journal and staff handover processes.")
        db.session.add(indotpoints7)
        db.session.commit()
        #2.4
        indotpoints8 = Dotpoints(sequence_id = 1, question_id =4, questionnaire_id = 1, section_id = 2, title = "Actively supports the residence behaviour management procedures.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 2, question_id =4, questionnaire_id = 1, section_id = 2, title = "Effectively and consistently manages student behaviour.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 3, question_id =4, questionnaire_id = 1, section_id = 2, title = "Effectively uses strategies for de-escalation of “at-risk” behaviour.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 4, question_id =4, questionnaire_id = 1, section_id = 2, title = "Manages the use of consequences and rewards sensitively and effectively.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 5, question_id =4, questionnaire_id = 1, section_id = 2, title = "Effectively uses restorative practice strategies.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 6, question_id =4, questionnaire_id = 1, section_id = 2, title = "Enforces the Residence policy in relation to responsible use of technology.")
        db.session.add(indotpoints8)
        indotpoints8 = Dotpoints(sequence_id = 7, question_id =4, questionnaire_id = 1, section_id = 2, title = "Knows when to refer a student to meet needs and uses the residence procedures for referrals.")
        db.session.add(indotpoints8)
        db.session.commit()
        #2.5
        indotpoints9 = Dotpoints(sequence_id = 1, question_id = 5, questionnaire_id =1, section_id =2,  title = "Values cultural diversity, and practices respect for other cultures.")
        db.session.add(indotpoints9)
        indotpoints9 = Dotpoints(sequence_id = 2, question_id = 5, questionnaire_id =1, section_id =2,  title = "Seeks to provide relevant and meaningful support in different cultural contexts.")
        db.session.add(indotpoints9)
        indotpoints9 = Dotpoints(sequence_id = 3, question_id = 5, questionnaire_id =1, section_id =2,  title = "Effectively manages inappropriate student behaviour towards other cultures.")
        db.session.add(indotpoints9)
        indotpoints9 = Dotpoints(sequence_id = 4, question_id = 5, questionnaire_id =1, section_id =2,  title = "Seeks to develop understanding of Aboriginal and Torres Strait Islander students’ cultural backgrounds.")
        db.session.add(indotpoints9)
        indotpoints9 = Dotpoints(sequence_id = 5, question_id = 5, questionnaire_id =1, section_id =2,  title = "Seeks to relate well with Aboriginal and Torres Strait Islander students and families.")
        db.session.add(indotpoints9)
        db.session.commit()
        #3.1
        indotpoints10 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id = 1, section_id = 3, title = "Shows respect and loyalty towards leadership.")
        db.session.add(indotpoints10)
        indotpoints10 = Dotpoints(sequence_id = 2, question_id = 1, questionnaire_id = 1, section_id = 3, title = "Follows direction from leadership.")
        db.session.add(indotpoints10)
        indotpoints10 = Dotpoints(sequence_id = 3, question_id = 1, questionnaire_id = 1, section_id = 3, title = "Provides constructive feedback to leadership.")
        db.session.add(indotpoints10)
        db.session.commit()
        #3.2
        indotpoints11 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Has effective, positive relationships with the boarding team, exhibiting courtesy and respect to all.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 2, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Utilises effective communication practices with the team.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 3, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Collaborates effectively with the team.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 4, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Attends team meetings and is punctual.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 5, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Makes positive contributions to team meetings.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 6, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Facilitates team meetings as required.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 7, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Follows current work rosters and is flexible to provide relief as required.")
        db.session.add(indotpoints11)
        indotpoints11 = Dotpoints(sequence_id = 8, question_id = 2, questionnaire_id = 1, section_id = 3, title = "Enables effective and punctual handovers.")
        db.session.add(indotpoints11)
        db.session.commit()
        #3.3
        indotpoints12 = Dotpoints(sequence_id = 1, question_id = 3, questionnaire_id = 1, section_id = 3, title = "Supports induction and shadowing as required for new team members.")
        db.session.add(indotpoints12)
        indotpoints12 = Dotpoints(sequence_id = 2, question_id = 3, questionnaire_id = 1, section_id = 3, title = "Supports new team members with guidance, encouragement and good role-modelling.")
        db.session.add(indotpoints12)
        db.session.commit()
        #4.1
        indotpoints13 = Dotpoints(sequence_id = 1, question_id = 1, questionnaire_id = 1, section_id = 4, title = "Completes all records and reports consistent with residence policies and procedures.")
        db.session.add(indotpoints13)
        indotpoints13 = Dotpoints(sequence_id = 2, question_id = 1, questionnaire_id = 1, section_id = 4, title = "Provides documentation on time and as requested, including medical records and maintenance requests.")
        db.session.add(indotpoints13)
        indotpoints13 = Dotpoints(sequence_id = 3, question_id = 1, questionnaire_id = 1, section_id = 4, title = "Written communication is neat and well written.")
        db.session.add(indotpoints13)
        db.session.commit()
        #4.2
        indotpoints14 = Dotpoints(sequence_id = 1, question_id = 2, questionnaire_id = 1, section_id = 4, title = "Communicates effectively with parents.")
        db.session.add(indotpoints14)
        indotpoints14 = Dotpoints(sequence_id = 2, question_id = 2, questionnaire_id = 1, section_id = 4, title = "Communicates effectively with school management and staff members.")
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

    # #set up email

    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = "test2022965@gmail.com"
    # app.config['MAIL_PASSWORD'] = "Test2022"
    # app.config['MAIL_USE_SSL'] = True
    # mail = Mail(app)
    
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

 
