#import modules
import os.path
import secrets
from PIL import Image
from flask import Blueprint, render_template, jsonify, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_admin import Admin
#from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from flask_mail import Mail, Message
from flask import redirect
import jinja2
import datetime
from datetime import datetime, time, date, timedelta, timezone
#from send_email import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy import asc, or_
from . import app



#from flask_uploads import UploadSet, configure_uploads, IMAGES
#set up Blueprint
views = Blueprint('views', __name__)

from .models import Subscription, db, User, Survey, Files, School, Manager, Questionnaire, Sections, Questions, Dotpoints, Response, Action, Comments, Evidence
from .forms import ApprovalForm, SurveyForm, EditProfileForm, EditUserForm, AppraisalForm, QueryManager, DeleteUserForm

#define schedule job
# @app.route("/success", methods=['POST'])
# def success():
#     scheduler.add_job(
#         send_email, DateTrigger(tduedate), args=(tnumber, company)
#     )

#Wordpress, Woocommerce API Key


#define webhook function for  
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        return jsonify(data), 200
    else:
        return abort (400)


# #define save picture function
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


#Create route for approval page
@app.route('/approval', methods=['GET', 'POST'])
#define approval function
def approval():
    form = ApprovalForm()
    #search all users where school id is equal to current user school id and is not approved or is a superuser
    users = User.query.filter_by(school_id=current_user.school_id, is_approved=False).all()

    
    for key, value in request.form.items():
        for u in users:
            if u.first_name == key:
                if value == "accept":
                    u.is_approved = True
                    db.session.commit()
                    flash('User has been approved', category = 'success' )
                elif value == 'reject':
                    db.session.delete(u)
                    db.session.commit()
                    flash('User has been rejected', category='success')
                break  
    
    return render_template('approval.html', users=users, form=form)
    

#define profile page 
@views.route("/profile", methods = ['GET','POST'])
#@login_required
def profile():
    form = EditProfileForm()
    #Get subscription for when school is is the same as current user school id
    subscription = Subscription.query.with_entities(Subscription.expiry_date).filter(Subscription.school_id==current_user.school_id).first()
    #convert Subscription.expiry_date value from the Subsciption table to date format
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.name = form.username.data
        current_user.licence = form.licence.data
        db.session.commit()
        flash("Your account has been updated!", category='success')
        return redirect(url_for('views.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html" ,image_file=image_file, form = form, subscription = subscription)

#define home page 
@views.route("/")
def home():   
    # #get the school id of the current user
    # user_s = current_user.school_id
    user = User()

    #Get the matching school name from the school table
    school = School.query.filter_by(id=user.school_id).first()
   
    return render_template("home.html", school =school, user = user)

#define create new appraisal page
@views.route("/appraisal/new", methods = ['GET','POST'])
#@login_required
def create_appraisal():
    #get the first query from the questionnaire table
    questionnaire = Questionnaire.query.filter_by(id=1).first()
    #Create empty list for sections
    lsec = []
    #Create empty dictionary for sections
    #Filter the sections table where the questionnaire id is equal to the questionnaire id
    sections = Sections.query.filter_by(questionnaire_id = questionnaire.id).all()
    ####Create a dictionary for sections, singular dictionary keys for the section id and one for the section name and value of elements in section table
    for sec in sections:
        #Create dictionary with values of section id and sections title
        dsec = {'section_id': sec.id, 'section_title': sec.title}
        dsec['questions'] = []

        #dsec = {section.id:section.id, section.title: section.title}
        #Filter the questions table where the questionnaire id is equal to the questionnaire id and section id is equal to the section id
        questions = Questions.query.filter_by(questionnaire_id = 1, section_id = sec.id).all()
        #Create a dictionary with question id key and question name key
        for ques in questions:
            dques = {'question_id': ques.id, 'question_title': ques.title}
            dques['dotpoints'] = []
            #Filter the dotpoints table where the questionnaire id is equal to the questionnaire id, section is is section id  and question id is equal to the question id
            dotpoints = Dotpoints.query.filter_by(questionnaire_id = 1, section_id = sec.id, question_id = ques.id).all()
            #Create a dictionary with dotpoint id key and dotpoint name key
            for dot in dotpoints:
                ddot = {'dotpoint_id': dot.sequence_id, 'dotpoint_name': dot.title}
                #Create empty list for dotpoints
                dques['dotpoints'].append(ddot)
            #Append question list to section dictionary
            dsec['questions'].append(dques)
        #Append section dictionary to list (list for multiple sections)
        lsec.append(dsec)

                
    review = ""
    evidence = ""
    comments = ""
    action = ""
    text = ""

    if request.method == 'POST':
         #Insert values into table response from Question table
    
        for key, value in request.form.items():
            if key.find('responses') == 0:
                name = 'responses'
            elif key.find('commentss') == 0:
                name = 'commentss'
            elif key.find('evidences') == 0:
                name = 'evidences'
            elif key.find('actions') == 0:
                name = 'actions'
            else:
                continue
            if key.find('q') == '-1':
                continue
            if (name == 'evidences' or name == 'actions'):
                if not current_user.is_superuser and not current_user.is_manager:
                    return 403
            section_num = key[len(name):key.find('q')]
            question_num = key[key.find('q') + 1:]
            if name == 'responses':
                resp = Response(questionnaire_id =1, section_id = section_num, question_id =question_num, user_id = current_user.id, rating = value )
                db.session.add(resp)
                db.session.commit()
            elif name == 'commentss':
                comm = Comments(questionnaire_id = 1, section_id = section_num, question_id = question_num, user_id = current_user.id, title = value)
                db.session.add(comm)
                db.session.commit()
            elif name == 'evidences':
                evi = Evidence(questionnaire_id = 1, section_id = section_num, question_id = question_num, user_id = current_user.id, title = value)
                db.session.add(evi)
                db.session.commit()
            else:
                act = Action(questionnaire_id = 1, section_id = section_num, question_id = question_num, user_id = current_user.id,  title = value)
                db.session.add(act)
                db.session.commit()
        flash("Your appraisal has been created!", category='success')
        return redirect(url_for('views.saved_reviews'))

    return render_template("create_review.html", lsec=lsec, text = text, review = review, evidence = evidence, comments = comments, action = action, questionnaire = questionnaire, sections = sections, questions = questions, dotpoints = dotpoints)

#Define appraisal form page
@views.route("/appraisal-form", methods = ['GET','POST'])
#@login_required
def appraisal_form():
    form = AppraisalForm()
    survey = Survey()
    
    #get the first query from the questionnaire table
    questionnaire = Questionnaire.query.filter_by(id=1).first()
    #Create empty list for sections
    lsec = []
    #Create empty dictionary for sections
    #Filter the sections table where the questionnaire id is equal to the questionnaire id
    sections = Sections.query.filter_by(questionnaire_id = questionnaire.id).all()
    ####Create a dictionary for sections, singular dictionary keys for the section id and one for the section name and value of elements in section table
    for sec in sections:
        #Create dictionary with values of section id and sections title
        dsec = {'section_id': sec.id, 'section_title': sec.title}
        dsec['questions'] = []

        #dsec = {section.id:section.id, section.title: section.title}
        #Filter the questions table where the questionnaire id is equal to the questionnaire id and section id is equal to the section id
        questions = Questions.query.filter_by(questionnaire_id = 1, section_id = sec.id).all()
        
        #Create a dictionary with question id key and question name key
        for ques in questions:
            dques = {'question_id': ques.id, 'question_title': ques.title}
            dques['dotpoints'] = []
            #Get query for completed rating and comments in response table
            rate = Response.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first()
            comm = Comments.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first()
            dques['rating'] = rate.rating
            dques['comments'] = comm.title
            #Filter the dotpoints table where the questionnaire id is equal to the questionnaire id, section is is section id  and question id is equal to the question id
            dotpoints = Dotpoints.query.filter_by(questionnaire_id = 1, section_id = sec.id, question_id = ques.id).all()
            #Create a dictionary with dotpoint id key and dotpoint name key
            for dot in dotpoints:
                ddot = {'dotpoint_id': dot.sequence_id, 'dotpoint_name': dot.title}
                #Create empty list for dotpoints
                dques['dotpoints'].append(ddot)
            #Append question list to section dictionary
            dsec['questions'].append(dques)
        #Append section dictionary to list (list for multiple sections)
        lsec.append(dsec)



                
    review = ""
    evidence = ""
    comments = ""
    action = ""
    text = ""

    if request.method == 'POST':
        # review = Response(title = form.choices.data 
         #Insert values into table response from Question table
    
        for key, value in request.form.items():
            if key.find('evidences') == 0:
                name = 'evidences'
            elif key.find('actions') == 0:
                name = 'actions'
            else:
                continue
            if key.find('q') == '-1':
                continue
            section_num = key[len(name):key.find('q')]
            question_num = key[key.find('q') + 1:]
            if name == 'evidences':
                evi = Evidence(questionnaire_id = 1, section_id = section_num, question_id = question_num, user_id = request.args['user'], date_posted = request.args['date'], title = value)
                db.session.add(evi)
                db.session.commit()
            else:
                act = Action(questionnaire_id = 1, section_id = section_num, question_id = question_num, user_id = request.args['user'], date_posted = request.args['date'], title = value)
                db.session.add(act)
                db.session.commit()
        flash("Your appraisal has been updated!", category='success')
        return redirect(url_for('views.managed_completed_reviews'))
    return render_template('appraisal_form.html', lsec = lsec, questionnaire = questionnaire) 

#Define appraisal display page
@views.route("/appraisal-display", methods = ['GET','POST'])
#@login_required
def appraisal_display():
    
    #get the first query from the questionnaire table
    questionnaire = Questionnaire.query.filter_by(id=1).first()
    #Create empty list for sections
    lsec = []
    #Create empty dictionary for sections
    #Filter the sections table where the questionnaire id is equal to the questionnaire id
    sections = Sections.query.filter_by(questionnaire_id = questionnaire.id).all()
    ####Create a dictionary for sections, singular dictionary keys for the section id and one for the section name and value of elements in section table
    for sec in sections:
        #Create dictionary with values of section id and sections title
        dsec = {'section_id': sec.id, 'section_title': sec.title}
        dsec['questions'] = []

        #dsec = {section.id:section.id, section.title: section.title}
        #Filter the questions table where the questionnaire id is equal to the questionnaire id and section id is equal to the section id
        questions = Questions.query.filter_by(questionnaire_id = 1, section_id = sec.id).all()
        
        #Create a dictionary with question id key and question name key
        for ques in questions:
            dques = {'question_id': ques.id, 'question_title': ques.title}
            dques['dotpoints'] = []
            #Get query for completed rating and comments in response table
            rate = Response.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first()
            comm = Comments.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first()
            evi  = Evidence.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first()
            act  = Action.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =request.args['user'], date_posted = request.args['date'] ).first() 
            dques['rating'] = rate.rating
            dques['comments'] = comm.title
            dques['evidence'] = evi.title
            dques['action'] = act.title
            #Filter the dotpoints table where the questionnaire id is equal to the questionnaire id, section is is section id  and question id is equal to the question id
            dotpoints = Dotpoints.query.filter_by(questionnaire_id = 1, section_id = sec.id, question_id = ques.id).all()
            #Create a dictionary with dotpoint id key and dotpoint name key
            for dot in dotpoints:
                ddot = {'dotpoint_id': dot.sequence_id, 'dotpoint_name': dot.title}
                #Create empty list for dotpoints
                dques['dotpoints'].append(ddot)
            #Append question list to section dictionary
            dsec['questions'].append(dques)
        #Append section dictionary to list (list for multiple sections)
        lsec.append(dsec)
                
    # review = ""
    # evidence = ""
    # comments = ""
    # action = ""
    # text = ""

    # if request.method == 'POST':
    #     # review = Response(title = form.choices.data 
    #      #Insert values into table response from Question table
    
    #     for key, value in request.form.items():
    #         if key.find('evidences') == 0:
    #             name = 'evidences'
    #         elif key.find('actions') == 0:
    #             name = 'actions'
    #         else:
    #             continue
    #         if key.find('q') == '-1':
    #             continue
    #         section_num = key[len(name):key.find('q')]
    #         question_num = key[key.find('q') + 1:]
            
    #     flash("Your appraisal has been updated!", category='success')
    #     return redirect(url_for('views.managed_reviews'))
    return render_template('appraisal_display.html', lsec = lsec, questionnaire = questionnaire) 
  
#Define appraisal display page
@views.route("/user-appraisal-display", methods = ['GET','POST'])
#@login_required
def user_appraisal_display():
    #Select Rating, Comment.title AS COMM, evidence.title AS EVID, action.title AS ACT from Response INNER JOIN COMMENT ON (Comment.user_id = Response.user_id AND Comment.date_posted = Response.date_posted) LEFT JOIN Evidence ON (Evidence.user_id = Response.user_id AND Evidence.date_posted = Response.date_posted) LEFT JOIN ACTION ON (Action.user_id = Response.user_id and Action.date_posted = Response.date_posted and Action.questionnaire_id = Response.questionnaire_id and Action.sec_id = Response.sec_id and Action.question_id = Response.question_id) WHERE Response.user_id = current_user.id AND Response.date_posted = #query string(request.args('date)) ORDERBY Response.sec_id asc, Response.quesion_id asc

    red = Response.query.filter_by(Response.user_id == current_user.id, Response.date_posted == request.args['date']).join(Comments, Comments.user_id == Response.user_id and Comments.date_posted == Response.date_posted and Comments.questionnaire_id == Response.questionnaire_id and Comments.section_id == Response.section_id and Comments.question_id == Response.question_id).outerjoin(Evidence, Evidence.user_id == Response.user_id, Evidence.date_posted == Response.date_posted, Evidence.questionnaire_id == Response.questionnaire_id, Evidence.section_id == Response.section_id, Evidence.question_id ==Response.question_id).outerjoin(Action, Action.user_id == Response.user_id, Action.date_posted == Response.date_posted, Action.questionnaire_id == Response.questionnaire_id, Action.section_id == Response.section_id, Action.question_id == Response.question_id).order_by(asc(Response.section_id), asc(Response.question_id))

    # get the first query from the questionnaire table
    questionnaire = Questionnaire.query.filter_by(id=1).first()
    #Crdbeate empty list for sections
    lsec = []
    #Create empty dictionary for sections
    #Filter the sections table where the questionnaire id is equal to the questionnaire id
    sections = Sections.query.filter_by(questionnaire_id = questionnaire.id).all()
    ####Create a dictionary for sections, singular dictionary keys for the section id and one for the section name and value of elements in section table
    for sec in sections:
        #Create dictionary with values of section id and sections title
        dsec = {'section_id': sec.id, 'section_title': sec.title}
        dsec['questions'] = []

        #Filter the questions table where the questionnaire id is equal to the questionnaire id and section id is equal to the section id
        questions = Questions.query.filter_by(questionnaire_id = 1, section_id = sec.id).all()
        
        #Create a dictionary with question id key and question name key
        for ques in questions:
            dques = {'question_id': ques.id, 'question_title': ques.title}
            dques['dotpoints'] = []
            #Get query for completed rating and comments in response table
            rate = Response.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =current_user.id, date_posted = request.args['date'] ).first()
            comm = Comments.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =current_user.id, date_posted = request.args['date'] ).first()
            evi  = Evidence.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =current_user.id, date_posted = request.args['date'] ).first()
            act  = Action.query.filter_by(questionnaire_id = 1, section_id =sec.id, question_id =ques.id, user_id =current_user.id, date_posted = request.args['date'] ).first() 
            dques['rating'] = rate.rating
            dques['comments'] = comm.title
            if evi != None:
                dques['evidence'] = evi.title
            if act != None:
                dques['actions'] = act.title
            #Filter the dotpoints table where the questionnaire id is equal to the questionnaire id, section is is section id  and question id is equal to the question id
            dotpoints = Dotpoints.query.filter_by(questionnaire_id = 1, section_id = sec.id, question_id = ques.id).all()
            #Create a dictionary with dotpoint id key and dotpoint name key
            for dot in dotpoints:
                ddot = {'dotpoint_id': dot.sequence_id, 'dotpoint_name': dot.title}
                #Create empty list for dotpoints
                dques['dotpoints'].append(ddot)
            #Append question list to section dictionary
            dsec['questions'].append(dques)
        #Append section dictionary to list (list for multiple sections)
        lsec.append(dsec)
   
    return render_template('user_appraisal_display.html', lsec = lsec, questionnaire = questionnaire, red = red) 

#define single appraisal page
@views.route("/appraisal/<int:review_id>")
def appraisal(review_id):
    review = Survey.query.get_or_404(review_id)
    return render_template("appraisal.html", title = review.title, review = review)

#Define about page
@views.route("/about")
def about():
    return render_template('about.html')

# #define saved reviews page 
@views.route("/saved-reviews")
def saved_reviews():
    #Select Rating, Comment.title AS COMM, evidence.title AS EVID, action.title AS ACT from Response INNER JOIN COMMENT ON (Comment.user_id = Response.user_id AND Comment.date_posted = Response.date_posted) LEFT JOIN Evidence ON (Evidence.user_id = Response.user_id AND Evidence.date_posted = Response.date_posted) LEFT JOIN ACTION ON (Action.user_id = Response.user_id and Action.date_posted = Response.date_posted and Action.questionnaire_id = Response.questionnaire_id and Action.sec_id = Response.sec_id and Action.question_id = Response.question_id) WHERE Response.user_id = current_user.id AND Response.date_posted = #query string(request.args('date)) ORDERBY Response.sec_id asc, Response.quesion_id asc
    rd = Response.query.with_entities(Response.date_posted).filter(Response.user_id == current_user.id).distinct(Response.date_posted).order_by(asc(Response.date_posted))
    
    return render_template('saved_reviews.html', rd = rd)


#define managed reviews page
@views.route("/managed-reviews")
def managed_reviews():
    if current_user.is_superuser:
        #Select user.id, DISTINCT response.date_posted FROM user LEFT JOIN response ON response.employee_id =user.id WHERE user.school_id = CURRENT_USER.school_id AND 0 IN (SELECT COUNT (*)) FROM evidence WHERE user_id = user.id AND evidence.date_posted = response.date_posted);
        #get reviews where school id is equal to current user school id
        emps =  User.query.with_entities(User.id).filter(User.school_id == current_user.school_id).all()
    elif current_user.is_manager:
        #emps =  SELECT employee from manager WHERE manager = current_user.id"
        emps = Manager.query.with_entities(Manager.employee_id).label('id').filter(Manager.manager_id ==current_user.id).all()
    else:
        return abort (403)
    Employees = []
    for e in emps:
        name = User.query.with_entities(User.first_name, User.last_name).filter(User.id == e.id).first()
        Employee = {'id': e.id, 'name':name.first_name + " " + name.last_name, }
        Employee['reviews'] = []
        # rev = SELECT distict date.posted FROM Response WHERE user.id = e.employee
        #SELECT DISTINCT response.date_posted FROM response LEFT JOIN evidence ON (evidence.user_id = response.user_id AND evidence.date_posted = response.date_posted) WHERE response.user_id = e.id AND evidence.title IS NULL;
        rev = Response.query.with_entities(Response.date_posted).outerjoin(Evidence, Evidence.date_posted == Response.date_posted and Evidence.user_id == Response.user_id).filter(Response.user_id == e.id).filter(Evidence.title == None).distinct(Response.date_posted).order_by(asc(Response.date_posted))
       
         #old one
        # rev = Response.query.with_entities(Response.date_posted).filter(Response.user_id == e.id).distinct(Response.date_posted).order_by(asc(Response.date_posted))
        for r in rev:
            Employee['reviews'].append(r.date_posted)
        Employees.append(Employee)
    return render_template('managed_reviews.html', Employees = Employees) 

    #define managed reviews page
@views.route("/managed-completed-reviews")
def managed_completed_reviews():
    if current_user.is_superuser:
        #get reviews where school id is equal to current user school id
        emps =  User.query.with_entities(User.id).filter(User.school_id == current_user.school_id).all()
    elif current_user.is_manager:
        #emps =  SELECT employee from manager WHERE manager = current_user.id"
        emps = Manager.query.with_entities(Manager.employee_id).label('id').filter(Manager.manager_id ==current_user.id).all()
    else:
        return abort (403)
    Employees = []
    for e in emps:
        name = User.query.with_entities(User.first_name, User.last_name).filter(User.id == e.id).first()
        Employee = {'id': e.id, 'name':name.first_name + " " + name.last_name, }
        Employee['reviews'] = []
        # rev = SELECT distict date.posted FROM Response WHERE user.id = e.employee
        rev = Response.query.with_entities(Response.date_posted).join(Evidence, Evidence.date_posted == Response.date_posted and Evidence.user_id == Response.user_id).join(Action, Action.date_posted == Response.date_posted and Action.user_id == Action.date_posted).filter(Response.user_id == e.id).filter(or_(Evidence.title != None, Action.title != None)).distinct(Response.date_posted).order_by(asc(Response.date_posted))
        # old one
        # rev = Response.query.with_entities(Response.date_posted).filter(Response.user_id == e.id).distinct(Response.date_posted).order_by(asc(Response.date_posted))
        for r in rev:
            Employee['reviews'].append(r.date_posted)
        Employees.append(Employee)
    return render_template('managed_completed_reviews.html', Employees = Employees) 
    
    
#define redirect-to-home route
@views.route("/direct_home")
def direct_home():
    return redirect(url_for("views.home"))


#define email reminder page * Change this
# @views.route("/email")
# def reminder():
#     msg = Message("Hello",
#                   sender="from@example.com",
#                   recipients=["to@example.com"])
#     msg.body = "Hi, this is a reminder to complete your review"
#     msg.html = "<b>reminder</b>"
#     mail.send(msg)

#define reminder route
# @views.route("/reminder")
# def reminder():
#     form = CombinedForm(request.form)  
#     if request.method == "POST" and form.validate():
#         due_date1 = form.date.data
#         due_date2  = form.date2.data
#         due_date3 = form.date3.data
#         due_date4 = form.date4.data


#define user table route
@views.route("/user-table", methods = ['GET','POST'])
def user_table():
    #Get forms
    form = EditUserForm()
    row = []
    managerform =  QueryManager()
    
   

    #Assign roles
    #get value of name {{user}} from form and assign to variable
    for key, value in request.form.items():

        id = ""
        if key.find('mymanager') == 0:
            id = key[len('mymanager')]
        elif key.find('manager') == 0:
            id = key[len('manager')]
        elif key.find('superuser') == 0:
            id = key[len('superuser')]
        elif id == "":
            continue

        uu = User.query.filter_by(school_id = current_user.school_id, is_approved = True, id = id).first()
        if (uu == None):
            continue

       
        if key.find('superuser') == 0:
            if value == "yes" and uu.is_superuser == False:
                uu.is_superuser = True
                db.session.commit()
            elif value == "no" and uu.is_superuser == True:
                uu.is_superuser = False
                db.session.commit()
            continue
        elif key.find('manager') == 0:
            if value == "yes" and uu.is_manager == False:
                uu.is_manager = True
                db.session.commit()
            elif value == "no" and uu.is_manager == True:
                uu.is_manager = False
                db.session.commit()
            continue
                    
        #Assign managers
        myman = Manager.query.filter_by(employee_id = id).first()
        if value == 'none':
            if myman != None:
                db.session.delete(myman)
                db.session.commit()
            continue
        if myman != None and value == myman.manager_id:
            continue
        validman = User.query.filter_by(id = value, school_id = current_user.school_id, is_approved = True, is_manager = True).first()
        if validman == None:
            continue
        if myman == None:
            m = Manager(employee_id = id, manager_id = value)
            db.session.add(m)
        else:
            myman.manager_id = value
        db.session.commit()

    # users = User.query.outerjoin(Manager, Manager.employee_id == User.id).filter(User.id != current_user.id).filter(User.school_id == current_user.school_id, User.is_approved == True).all()
    users = db.session.query(User.id, User.first_name, User.last_name, User.email, User.is_manager, User.is_superuser, Manager.manager_id).select_from(User).outerjoin(Manager, Manager.employee_id == User.id).filter(User.id != current_user.id).filter(User.school_id == current_user.school_id, User.is_approved == True).all()
   
    #Get managers whose school id is the same as current user from the manager table
    available_managers = User.query.filter_by(school_id = current_user.school_id, is_approved = True, is_manager = True).all()
    return render_template("table.html", users = users, available_managers = available_managers)


#Define edit user route
@views.route("/user/<int:id>/edit", methods=['GET','POST'])
def edit_user(id):
    #get users from user table that are approved and have the same school id as current user
    user = User.query.get_or_404(id)
    form = EditUserForm()
    if request.method == "POST" and form.validate():
        current_user.name = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        if form.delete.data == True:
            db.session.delete(user)
            db.session.commit()
            flash('User has been rejected', category='success')
        flash('Your changes have been saved')
        return redirect(url_for('views.user_table'))
    return render_template("edit_user.html", form = form, user = user)


# #define delete_user route
@views.route("/delete_user/<int:id>", methods = ['GET','POST'])
def delete_user(id):
    #get users from user table that are approved and have the same school id as current user
    user = User.query.get_or_404(id)
    form = DeleteUserForm()
    if request.method == "POST" and form.validate():
        if form.delete.data == True:
            db.session.delete(user)
            db.session.commit()
            flash('User has been rejected', category='success')
        return redirect(url_for('views.user_table'))
    return render_template("delete_user.html", form = form, user = user)


 #Define select Query Manager route
@views.route("/select_manager", methods = ['GET','POST'])
def select_manager():
    form = QueryManager()
    #get users from user table that are approved and have the same school id as current user
    users = User.query.filter_by(is_approved = True, school_id = current_user.school_id).all()
    #filter users by users that don't have the same id as current user
    users = [user for user in users if user.id != current_user.id]
    #get managers from manager table
    managers = Manager.query.all()
    #get reviews from survey table
    reviews = Survey.query.all()
    #if form is submitted
    if request.method == "POST" and form.validate():
        #get manager id from form
        manager_id = form.manager.data
        #get manager name from manager table where manager id is equal to manager id from form
        manager_name = Manager.query.filter_by(id = manager_id).first()
        #get user id from form
        user_id = form.User.data
        #get user name from user table where user id is equal to user id from form
        user_name = User.query.filter_by(id = user_id).first()
        
      

# #define appraisal matrix page 
# @views.route("/create-appraisal")
# def matrix():
#     return render_template("supervisor_practice.html")

