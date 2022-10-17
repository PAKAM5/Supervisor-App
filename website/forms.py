from flask import Flask, Request
from flask_wtf import FlaskForm
from flask_login import current_user
import wtforms
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField, RadioField, FileField, widgets
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms.fields import DateField, EmailField, TelField
from .models import User



#Edit profile form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    licence = StringField ('Licences')
    position = StringField('Position')
    picture = FileField('Update Profile Picture(only accept *.jpg,*.png)', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(name=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

#Survey Form
class SurveyForm(FlaskForm):
    title = StringField('Title')
    document = FileField('Upload Document', validators=[FileAllowed(['pdf', 'docx', 'doc', 'txt'])])
    choices = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date = DateField('Due Date', format='%Y-%m-%d')
    choices2 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments2 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence2 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions2 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date2 = DateField('Due Date', format='%Y-%m-%d')
    choices3 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments3 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence3 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions3 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date3 = DateField('Due Date', format='%Y-%m-%d')
    choices4 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments4 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence4 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions4 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date4 = DateField('Due Date', format='%Y-%m-%d')
    choices5 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments5 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence5 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions5 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date5 = DateField('Due Date', format='%Y-%m-%d')
    choices6 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments6 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence6 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions6 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date6 = DateField('Due Date', format='%Y-%m-%d')
    choices7 = RadioField('Label', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments7 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence7 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions7 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date7 = DateField('Due Date', format='%Y-%m-%d')
    choices8 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments8 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence8 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions8 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date8 = DateField('Due Date', format='%Y-%m-%d')
    choices9 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments9 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence9 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions9 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date9 = DateField('Due Date', format='%Y-%m-%d')
    choices10 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments10 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence10 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions10 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date10 = DateField('Due Date', format='%Y-%m-%d')
    choices11 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments11 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence11 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions11 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date11 = DateField('Due Date', format='%Y-%m-%d')
    choices12 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments12 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence12 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions12 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date12 = DateField('Due Date', format='%Y-%m-%d')
    choices13 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments13 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence13 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions13 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date13 = DateField('Due Date', format='%Y-%m-%d')
    choices14 = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments14 = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence14 = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions14 = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date14 = DateField('Due Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')

#class appraisal form
class AppraisalForm(FlaskForm):
    title = StringField()
    choices = RadioField('Choices', choices = [('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    comments = TextAreaField('Comments', validators=[Length(min=0, max=200)])
    evidence = TextAreaField('Evidence', validators=[Length(min=0, max=200)])
    actions = TextAreaField('Actions', validators=[Length(min=0, max=200)])
    date = DateField('Due Date', format='%Y-%m-%d')
    submit = SubmitField('Submit')





class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ApprovalForm(FlaskForm):

    accept = RadioField('Choices', choices = [('accept','accept'),('reject','reject'),('defer','defer')])

    submit = SubmitField("Submit")
    

    




# #Professional Practice Form
# class Professional(FlaskForm):
#     title = BooleanField("1.1 Aware of and complies with current legislation relevant to the role")
#     choices = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments = TextAreaField('Comments')
#     evidence = TextAreaField('Evidence')
#     actions = TextAreaField('Actions')
#     date = DateField('Due Date', format='%Y-%m-%d')
#     title2 = BooleanField("1.2 1.2 Aware of and complies with organisation requirements")
#     choices2 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments2 = TextAreaField('Comments')
#     evidence2 = TextAreaField('Evidence')
#     actions2 = TextAreaField('Actions')
#     date2 = DateField('Due Date', format='%Y-%m-%d')
#     title3 = BooleanField("1.3 Relevant professional learning completed")
#     choices3 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments3 = TextAreaField('Comments')
#     evidence3 = TextAreaField('Evidence')
#     actions3 = TextAreaField('Actions')
#     date3 = DateField('Due Date', format='%Y-%m-%d')
#     title4 = BooleanField("1.4 Safe Workplace health and safety practices")
#     choices4 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments4 = TextAreaField('Comments')
#     evidence4 = TextAreaField('Evidence')
#     actions4 = TextAreaField('Actions')
#     date4 = DateField('Due Date', format='%Y-%m-%d')
#     submit = SubmitField('Confirm')
    
# #Supervision Form
# class Supervision(FlaskForm):
#     title = BooleanField("2.1 Contributes to safe activities and environment for all boarders.")
#     choices = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments = TextAreaField('Comments')
#     evidence = TextAreaField('Evidence')
#     actions = TextAreaField('Actions')
#     date = DateField('Due Date', format='%Y-%m-%d')
#     title2 = BooleanField("2.2 Has respectful professional relationships with all boarders.")
#     choices2 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments2 = TextAreaField('Comments')
#     evidence2 = TextAreaField('Evidence')
#     actions2 = TextAreaField('Actions')
#     date2 = DateField('Due Date', format='%Y-%m-%d')
#     title3 = BooleanField("2.3 Supervises boarders effectively, supporting and meeting needs")
#     choices3 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments3 = TextAreaField('Comments')
#     evidence3 = TextAreaField('Evidence')
#     actions3 = TextAreaField('Actions')
#     date3 = DateField('Due Date', format='%Y-%m-%d')
#     title4 = BooleanField("2.4 Facilitates positive boarder behaviours")
#     choices4 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments4 = TextAreaField('Comments')
#     evidence4 = TextAreaField('Evidence')
#     actions4 = TextAreaField('Actions')
#     date4 = DateField('Due Date', format='%Y-%m-%d')
#     title5 = BooleanField("2.5 Provides sensitive appropriate cultural support")
#     choices5 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments5 = TextAreaField('Comments')
#     evidence5 = TextAreaField('Evidence')
#     actions5 = TextAreaField('Actions')
#     date5 = DateField('Due Date', format='%Y-%m-%d')
#     submit = SubmitField('Confirm')

# #Team Form
# class Team(FlaskForm):
#     title = BooleanField("1.1 Aware of and complies with current legislation relevant to the role")
#     choices = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments = TextAreaField('Comments')
#     evidence = TextAreaField('Evidence')
#     actions = TextAreaField('Actions')
#     date = DateField('Due Date', format='%Y-%m-%d')
#     title2 = BooleanField("1.2 1.2 Aware of and complies with organisation requirements")
#     choices2 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments2 = TextAreaField('Comments')
#     evidence2 = TextAreaField('Evidence')
#     actions2 = TextAreaField('Actions')
#     date2 = DateField('Due Date', format='%Y-%m-%d')
#     title3 = BooleanField("1.3 Relevant professional learning completed")
#     choices3 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
#     comments3 = TextAreaField('Comments')
#     evidence3 = TextAreaField('Evidence')
#     actions3 = TextAreaField('Actions')
#     date3 = DateField('Due Date', format='%Y-%m-%d')
#     submit = SubmitField('Confirm')

# #Administration Form  
# class Administration(FlaskForm):
    # title = BooleanField("1.1 Aware of and complies with current legislation relevant to the role")
    # choices = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    # comments = TextAreaField('Comments')
    # evidence = TextAreaField('Evidence')
    # actions = TextAreaField('Actions')
    # date = DateField('Due Date', format='%Y-%m-%d')
    # title2 = BooleanField("1.2 1.2 Aware of and complies with organisation requirements")
    # choices2 = RadioField('Label', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    # comments2 = TextAreaField('Comments')
    # evidence2 = TextAreaField('Evidence')
    # actions2 = TextAreaField('Actions')
    # date2 = DateField('Due Date', format='%Y-%m-%d')
    # submit = SubmitField('submit')

#Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[DataRequired(), Email()])
    school_id = StringField('Input School ID')
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

#Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
#Upload Form
class UploadForm(FlaskForm):
    file = FileField('Appraisal matrix', validators=[
        FileRequired(),
        FileAllowed('pdf', 'Upload supervisor appraisal matrix')
    ])
    filename = StringField('Filename')
    submit = SubmitField('Upload')

# #Create a form combining Professional, Supervision, Administration, Team forms
# class CombinedForm(FlaskForm):
    # professional = wtforms.FormField(Professional)
    # supervision = wtforms.FormField(Supervision)
    # team = wtforms.FormField(Team)
    # administration = wtforms.FormField(Administration)


#EditUser Form
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    is_manager = BooleanField('Manager')
    is_superuser = BooleanField('Superuser')
    delete = BooleanField('Delete')
    submit = SubmitField('Update')

##Select * from sections where questionionnaire = 1, orderedby section_number (Ascending)
##HTML -  section_number, section_name
##Select * questions where questionnaire = 1 and section_number =  questionnaire.section_number orderedby  question_number ascending
##HTML section_number.question.question_number.question_title.
##select * from dotpoints where questionnaire = 1
# and section = questionnaire.section_num
# and question = current.section.question_number orderedby sequence_number ascending
