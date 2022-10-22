#import modules
from flask import Blueprint, render_template, request, flash, redirect, url_for  
from flask_login import LoginManager, login_user, login_required, current_user, logout_user 
from werkzeug.security import generate_password_hash

from website.forms import LoginForm, RegistrationForm

auth = Blueprint('auth', __name__)

#import views

from .views import views

#import models

from .models import db, User

#import other modules

from .__init__ import app, bcrypt


#Define authentication approval request route
# @auth.route('/approval', methods=['GET', 'POST'])
# def approval():
#     user = User()
#     if user.is_approved:


#define login
@auth.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.profile'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user, remember = form.remember.data)
                if current_user.is_approved:
                    flash("You are logged in")
                    return redirect(url_for('views.profile')) 
                else:
                    logout_user()
                    flash("You are not approve, please wait to be approved by your Head of Boarding") 
    return render_template('login.html', form = form)

#define logout
@auth.route('/logout')
def logout():
    logout_user()
    return render_template("home.html")


#define sign up
@auth.route("/sign-up", methods = ['GET','POST'])
def sign_up():
    #Get submissions from signup post
    if current_user.is_authenticated:
        return redirect(url_for('views.profile'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
            new_user = User (school_id = form.school_id.data, name = "Employee", phone = form.phone.data, email = form.email.data, password = form.password.data, first_name = form.first_name.data, last_name = form.last_name.data, is_approved = False )
            db.session.add(new_user)
            db.session.commit()
            flash ('Your account is pending please wait for approval by your Head of Boarding', category = 'success')
            return render_template('approval_pending.html')
    return render_template('sign_up.html', form = form)




