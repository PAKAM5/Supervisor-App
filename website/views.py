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
from sqlalchemy import asc
from . import app



#from flask_uploads import UploadSet, configure_uploads, IMAGES
#set up Blueprint
views = Blueprint('views', __name__)

from .models import db, User, Survey, Files, School, Manager, Questionnaire, Sections, Questions, Dotpoints, Response, Action, Comments, Evidence
from .forms import ApprovalForm, SurveyForm, EditProfileForm, EditUserForm, AppraisalForm, QueryManager

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
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.username.data
        current_user.email = form.email.data
        current_user.licence = form.licence.data
        db.session.commit()
        flash("Your account has been updated!", category='success')
        return redirect(url_for('views.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("profile.html" ,image_file=image_file, form = form)

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

    return render_template("create_review.html", lsec=lsec, dsec = dsec, form = form, text = text, review = review, evidence = evidence, comments = comments, action = action, questionnaire = questionnaire, sections = sections, questions = questions, dotpoints = dotpoints)


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
    #select distinct dateposted from Response table where user id is equal to current_user

    #select distinct value from date_posted column from Response table where user id is equal to current_user
    rd = Response.query.with_entities(Response.date_posted).filter(Response.user_id == current_user.id).distinct(Response.date_posted).order_by(asc(Response.date_posted))


    return render_template('saved_reviews.html', rd = rd)


#define managed reviews page
@views.route("/managed-reviews")
def managed_reviews():
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
        rev = Response.query.with_entities(Response.date_posted).filter(Response.user_id == e.id).distinct(Response.date_posted).order_by(asc(Response.date_posted))
        for r in rev:
            Employee['reviews'].append(r.date_posted)
        Employees.append(Employee)
    return render_template('managed_reviews.html', Employees = Employees) 
    
    
#define redirect-to-home route
@views.route("/direct_home")
def direct_home():
    return redirect(url_for("views.home"))

# #define file upload page
# @views.route("/upload", methods = ['GET','POST'])
# def file_upload():
#     form = UploadForm()
#     if form.validate_on_submit():
#         file = Files()
#         form.populate_obj(file)
#         db.session.add(file)
#         db.session.commit()
#         flash ('Your file has been uploaded')
#         return redirect(('saved_reviews'))
#     return render_template("upload.html", form = form)

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
    #get users from user table that are approved and have the same school id as current user but are not superuser
    # userspre = User.query.filter_by(is_approved = True, school_id = current_user.school_id).all()
    #Get users from user table that are not current user
    users = User.query.filter(User.id != current_user.id).filter_by(school_id = current_user.school_id, is_approved = True).all()
    #Get managers whose school id is the same as current user from the manager table
    available_managers = User.query.filter(User.id != current_user.id).filter_by(school_id = current_user.id, is_approved = True, is_manager = True).all()
    # available_managers = Manager.query.filter_by(school_id = current_user.school_id).all()
    #Now forming the list of tuples for SelectField
    manager_list=[(i.id, i.name) for i in available_managers]
    managerform.manager_id.choices = manager_list
 
    #Assign roles
    #get value of name {{user}} from form and assign to variable
    for key, value in request.form.items():


        id = ""
        if key.find('manager') == 0:
            id = key[len('manager')]
        elif key.find('superuser') == 0:
            id = key[len('superuser')]
        elif id == "":
            continue

        for user in users:
            if user.id == id:
                if key[0] == 's':
                    user.is_superuser = True
                    db.session.commit()

                elif key[0] == 'manager':
                    user.is_manager = True
                    db.session.commit()
                    add_manager = Manager(name = user.name, school_id = user.school_id, id = user.id)
                    db.session.add(add_manager)
                    db.session.commit()
                

        



        #if the user id is equal to the current user id
        # if form.is_manager.data == True:
        #     row.is_manager = True
        #     db.session.commit()
        #     #add row name to manager name in manage table
        #     add_manager = Manager(name = row.name, school_id = row.school_id, id = row.id)
        #     db.session.add(add_manager)
        #     db.session.commit()
        # if form.is_superuser.data == True:
        #     row.is_superuser = True
        #     db.session.commit()
        # elif form.is_manager.data == False:
        #     row.is_manager = False
        #     db.session.commit()
        #     #remove row name from manager name in manage table
        #     if row.name == Manager.name: 
        #         remove_manager = Manager.query.filter_by(name = row.name).first()
        #         db.session.delete(remove_manager)
        #         db.session.commit()
        # elif form.is_superuser.data == False:
        #     row.is_superuser = False
        #     db.session.commit()
        #Assign Managers
    # for row in users:
    #     for i in managerform.manager_id.choices:
    #         i.id = row.manager_id
    #         db.session.commit()
        # for i in manager_list:
        #     if i.id in row:   
    return render_template("table.html", users = users, form = form, managerform = managerform)


#Define delete user route
@views.route("/user/<int:id>/delete", methods=['GET','POST'])
def delete_user(id):
    #get users from user table that are approved and have the same school id as current user
    user = User.query.get_or_404(id)
    form = EditUserForm()
    if request.method == "POST" and form.validate():
        current_user.name = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        if form.delete.data == True:
            db.session.delete(user)
            db.session.commit()
            flash('User has been rejected', category='success')
        flash('Your changes have been saved')
        return redirect(url_for('views.user_table'))
    return render_template("edit_user.html", form = form, user = user)


# #define edit_user route
@views.route("/edit_user/<int:id>", methods = ['GET','POST'])
def edit_user(id):
    #get users from user table that are approved and have the same school id as current user
    user = User.query.get_or_404(id)
    form = EditUserForm()
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

