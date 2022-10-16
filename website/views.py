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
from datetime import datetime
from datetime import time
from datetime import date
from datetime import timedelta
#from send_email import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from . import app



#from flask_uploads import UploadSet, configure_uploads, IMAGES
#set up Blueprint
views = Blueprint('views', __name__)

from .models import db, User, Survey, Files, School, Questionnaire, Sections, Questions, Dotpoints, Response, Action, Comments, Evidence
from .forms import ApprovalForm, SurveyForm, EditProfileForm, EditUserForm, AppraisalForm

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

    for user in users:
        # for user in users:
        if form.accept.data == 'accept':
            user.is_approved = True
            db.session.commit()
            flash('User has been approved', category='success')
        elif form.accept.data == 'reject':
            db.session.delete(user)
            db.session.commit()
            flash('User has been rejected', category='success')
        elif form.accept.data == 'defer':
            user.is_approved = False
            db.session.commit()
            flash('User has been deferred', category='success')
        duser = {'user': user}
    
    
      # login_user(users, accept = form.accept.data)
    
    return render_template('approval.html',user = user, users=users, duser =duser, form=form)
    

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
        dsec = {'section_id ': sec.id, 'section_title': sec.title}
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
                ldot = []
                #Append dotpoint dictionary to list (create list for multiple dotpoints)
                ldot.append(ddot)
                #Add dotpoint list to question dictionary
                dques['dotpoints'] = ldot
                #Append question list to section dictionary
                dsec['questions'].append(dques)
                #Append section list to s
                #Append section dictionary to list (list for multiple sections)
                lsec.append(dsec)
                    
    
    review = []
    evidence = []
    comments = []
    action = []
    text = ""


    if form.validate_on_submit() and request.method == 'POST':
        # review = Response(title = form.choices.data )
       #create for loop for entry in choices

       
        for row in form.choices.data.items:  
            review = Response(title = row )
            db.session.add(review)
            db.session.commit()
        #Create for loop for every entry in Evidence

        for row in form.evidence.data.items:
            evidence = Evidence(title = row )
            db.session.add(evidence)
            db.session.commit()
        #Create for loop for every entry in Comments

        for row in form.comments.data.items:
            comments = Comments(title = row )
            db.session.add(comments)
            db.session.commit()
        #Create for loop for every entry in Action

        for row in form.actions.data.items:
            action = Action(title = row )
            db.session.add(action)
            db.session.commit()
        flash("Your appraisal has been created!", category='success')
        return redirect(url_for('views.saved_reviews'))

    return render_template("create_review.html", lsec=lsec, dsec = dsec, form = form, text = text, review = review, evidence = evidence, comments = comments, action = action, questionnaire = questionnaire, sections = sections, questions = questions, dotpoints = dotpoints)



# #define create new appraisal page
# @views.route("/appraisal/new", methods = ['GET','POST'])
# #@login_required
# def create_appraisal():
#     form = SurveyForm()
#     if form.validate_on_submit() and request.method == 'POST':
#         review = Survey( author = current_user, title = form.title.data, choices = form.choices.data, comments = form.comments.data, evidence = form.evidence.data, actions = form.actions.data,
#         choices2 = form.choices2.data, comments2 = form.comments2.data, evidence2 = form.evidence2.data, actions2 = form.actions2.data,
#         choices3 = form.choices3.data, comments3 = form.comments3.data, evidence3 = form.evidence3.data, actions3 = form.actions3.data,
#         choices4 = form.choices4.data, comments4 = form.comments4.data, evidence4 = form.evidence4.data, actions4 = form.actions4.data,
#         choices5 = form.choices5.data, comments5 = form.comments5.data, evidence5 = form.evidence5.data, actions5 = form.actions5.data,
#         choices6 = form.choices6.data, comments6 = form.comments6.data, evidence6 = form.evidence6.data, actions6 = form.actions6.data,
#         choices7 = form.choices7.data, comments7 = form.comments7.data, evidence7 = form.evidence7.data, actions7 = form.actions7.data,
#         choices8 = form.choices8.data, comments8 = form.comments8.data, evidence8 = form.evidence8.data, actions8 = form.actions8.data,
#         choices9 = form.choices9.data, comments9 = form.comments9.data, evidence9 = form.evidence9.data, actions9 = form.actions9.data,
#         choices10 = form.choices10.data, comments10 = form.comments10.data, evidence10 = form.evidence10.data, actions10 = form.actions10.data,
#         choices11 = form.choices11.data, comments11 = form.comments11.data, evidence11 = form.evidence11.data, actions11 = form.actions11.data,
#         choices12 = form.choices12.data, comments12 = form.comments12.data, evidence12 = form.evidence12.data, actions12 = form.actions12.data,
#         choices13 = form.choices13.data, comments13 = form.comments13.data, evidence13 = form.evidence13.data, actions13 = form.actions13.data,
#         choices14 = form.choices14.data, comments14 = form.comments14.data, evidence14 = form.evidence14.data, actions14 = form.actions14.data,)
#         db.session.add(review)
#         db.session.commit()
#         flash ('Your survey has been saved', "success")
#         return redirect('/saved-reviews')
#     return render_template("create_appraisal.html", title = "Create New Appraisal", form = form)

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
    #get reviews from survey table where author is current user
    reviews = Survey.query.filter_by(author = current_user).all()
    
    # reviews = Survey.query.all()
    return render_template('saved_reviews.html', reviews = reviews)


#define managed reviews page
@views.route("/managed-reviews")
def managed_reviews():
    if current_user.is_superuser:
        #get reviews where school id is equal to current user school id
        reviews = Survey.query.filter_by(school_id = current_user.school_id).all()
        # reviews = Survey.query.all()
        return render_template("managed_reviews.html", reviews = reviews)
    elif current_user.is_manager:
        #Get reviews where supervisor manager id is equal to current user id
        reviews = Survey.query.filter_by(manager_id = current_user.manager_id).all()
        # reviews = Survey.query.all()
        return render_template("managed_reviews.html", reviews = reviews)
    else:
        return abort (403)
    
    
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
    form = EditUserForm()
    #get users from user table that are approved and have the same school id as current user but are not superuser
    #  users = User.query.filter_by(is_approved = True, school_id = current_user.school_id, is_superuser = False).all()
    users = User.query.filter_by(is_approved = True, school_id = current_user.school_id).all()
    #filter users by users that don't have the same id as current user
    
    for row in users:
        #if the user id is equal to the current user id
        if form.is_manager.data == True:
            row.is_manager = True
            db.session.commit()
        elif form.is_superuser.data == True:
            row.is_superuser = True
            db.session.commit()
        elif form.is_manager.data == False:
            row.is_manager = False
            db.session.commit()
        elif form.is_superuser.data == False:
            row.is_superuser = False
            db.session.commit()
    return render_template("table.html", row=row, users = users, form = form)

#Define delete user route
@app.route("/user/<int:id>/delete", methods=['GET','POST'])
def delete_user(id):
    if request.method == 'POST':
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return render_template("table.html", id = id, user = user)



# #define edit_user route
@views.route("/edit_user/<int:id>", methods = ['GET','POST'])
def edit_user(id):
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
      

# #define appraisal matrix page 
# @views.route("/create-appraisal")
# def matrix():
#     return render_template("supervisor_practice.html")

