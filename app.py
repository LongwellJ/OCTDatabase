from flask import Flask, render_template, flash, request, redirect, url_for, send_file
from datetime import datetime 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash 
from datetime import date
from webforms import LoginForm, PostForm, UserForm, PasswordForm, SearchForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from webforms import PostForm, LoginForm, UserForm, PasswordForm, SearchForm, DobForm, IDForm, UpdateForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os
import boto3
import botocore.session
from datetime import datetime
import pandas as pd
from uuid import uuid4
import numpy as np

DATABASE_URL = os.environ.get('DATABASE_URL', 'fallback_url_if_not_found')

# Create a Flask Instance
app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)
# Add Database
# Old SQLite DB
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SESSION_COOKIE_SECURE'] = True

# New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/our_users'
# Secret Key!
app.config['SECRET_KEY'] = "test"
# Initialize The Database

UPLOAD_FOLDER = 'static/images/'
INPUT_PATH= './Input/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Boto3 Stuff
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    region_name='ca-central-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

clientsession = botocore.session.Session()
clientsession.set_credentials(
    
    access_key='test',
    secret_key='test',
    token=None,
)
s3_client = clientsession.create_client('s3',region_name='ca-central-1')

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

#Create a credits page
@app.route('/credits')
@login_required
def credits():
    return render_template("credits.html")
# Create Admin Page
@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id == 1:
		return render_template("admin.html")
	else:
		flash("Sorry you must be the Admin to access the Admin Page...")
		return redirect(url_for('dashboard'))

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Succesfull!!")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("That User Doesn't Exist! Try Again...")


	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You Have Been Logged Out!  Thanks For Stopping By...")
	return redirect(url_for('login'))

# Create Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    id = current_user.id
    return render_template('dashboard.html',id=id)

#Create an index page
@app.route('/')
@login_required
def index():

    flash("Welcome to your database!")
    user = current_user.id
    
    return redirect(url_for("allpatients", user = user))

# Showing data to user in table
@app.route('/allpatients/<int:user>', methods=['GET', 'POST'])
@login_required
def allpatients(user):
    if current_user.id == 1:
        user = 1
        theposts = Posts.query.all()
        df = pd.DataFrame(columns=[["Patient's Study Identifiers", "Patient's Study Identifiers", "Patient's Study Identifiers", "Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I", "Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II", "1 Week Post-Op","1 Week Post-Op","1 Week Post-Op","1 Month Post-Op","1 Month Post-Op","1 Month Post-Op", "3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","Single procedure anatomical Success", "6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","Final procedure anatomical Success","Final procedure anatomical Success"],
                                                            ["Database ID", "First Names' Letters", "DOB", "Age","Gender","Laterality (OD/OS)","Date","Fovea Status (Off / Split / On)","When did the shadow first appear? (in days)","When did the shadow first involved the central vision field? (in days)","Lens status (phakic/ pseudophakic/ aphakic)","Extent of the detachment (clock hours: hh:mm1-hh:mm2)","Main area of the detachment (sup/ inf/ total)","Number and Locations of retinal tears detached (number-clock hour, number-clock hour,.. )","Number and Locations of retinal tears attached (number-clock hour, number-clock hour,.. )","Size of the largest tear (optic disc measurment)","BCVA (snellen)","IOP (mmHg)","PVD status (Y/N)","PVR status (if yes, stage A/B/Ca/Cp)","Presence of vitreous hemorrhage (graded on a 5-point scale from 0 to 4)", "Date (dd/mm/yyyy)","Procedure type (PPV/ SB / PPV+SB)","Combined PhakoVitrectomy? (Y/N)","Cryo (Y/N)","Laser (number of pulses, energy (in mW), time (in seconds))","Drainage Technique (P- peripheral /R- retinotomy)","Tamponade used (Material, Volume)","PFO fluid (Y/N)","Number and Locations of retinal tears detached found Intra operativly (number-clock hour, number-clock hour,.. )", "Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)","Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)","Is there silicone oil in the eye?"]])
        for row in theposts:
            #print(row.dateofbirth)
            tuple_data = (row.id,row.firstandlast,row.dateofbirth,row.age,row.gender,row.laterality,row.date1,row.fovea_status,row.shadow,row.involved,row.lens_status,row.extent,row.area,row.detachedtotal,row.attachedtotal,row.size,row.bcva,row.iop,row.pvd,row.pvr,row.hemorrhage,row.date2,row.type,row.combined,row.cryo,row.laser,row.tech,row.tamp,row.pfo,row.found,row.date3,row.bcva2,row.iop2,row.date4,row.bcva3,row.iop3,row.date5,row.lens_status2,row.bcva4,row.iop4,row.m_charth,row.m_chartv,row.ask,row.questionnaire,row.acheive,row.date6,row.lens_status3,row.bcva5,row.iop5,row.m_charth2,row.m_chartv2,row.ask2,row.questionnaire2,row.date7,row.lens_status4,row.bcva6,row.iop6,row.m_charth3,row.m_chartv3,row.ask3,row.questionnaire3,row.acheive2, row.oil)
            newrow = pd.DataFrame([tuple_data],columns=[["Patient's Study Identifiers", "Patient's Study Identifiers", "Patient's Study Identifiers", "Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I", "Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II", "1 Week Post-Op","1 Week Post-Op","1 Week Post-Op","1 Month Post-Op","1 Month Post-Op","1 Month Post-Op", "3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","Single procedure anatomical Success", "6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","Final procedure anatomical Success","Final procedure anatomical Success"],["Database ID", "First Names' Letters", "DOB", "Age","Gender","Laterality (OD/OS)","Date","Fovea Status (Off / Split / On)","When did the shadow first appear? (in days)","When did the shadow first involved the central vision field? (in days)","Lens status (phakic/ pseudophakic/ aphakic)","Extent of the detachment (clock hours: hh:mm1-hh:mm2)","Main area of the detachment (sup/ inf/ total)","Number and Locations of retinal tears detached (number-clock hour, number-clock hour,.. )","Number and Locations of retinal tears attached (number-clock hour, number-clock hour,.. )","Size of the largest tear (optic disc measurment)","BCVA (snellen)","IOP (mmHg)","PVD status (Y/N)","PVR status (if yes, stage A/B/Ca/Cp)","Presence of vitreous hemorrhage (graded on a 5-point scale from 0 to 4)", "Date (dd/mm/yyyy)","Procedure type (PPV/ SB / PPV+SB)","Combined PhakoVitrectomy? (Y/N)","Cryo (Y/N)","Laser (number of pulses, energy (in mW), time (in seconds))","Drainage Technique (P- peripheral /R- retinotomy)","Tamponade used (Material, Volume)","PFO fluid (Y/N)","Number and Locations of retinal tears detached found Intra operativly (number-clock hour, number-clock hour,.. )", "Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)","Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)","Is there silicone oil in the eye?"]])
        
            df = pd.concat([df,newrow], ignore_index=True)
        df.to_excel('data.xlsx')    
        return render_template("allpatients.html",user = user, theposts=theposts)

    elif user == current_user.id:
    
        theposts = Posts.query.filter_by(poster_id = user)
        df = pd.DataFrame(columns=[["Patient's Study Identifiers", "Patient's Study Identifiers", "Patient's Study Identifiers", "Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I", "Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II", "1 Week Post-Op","1 Week Post-Op","1 Week Post-Op","1 Month Post-Op","1 Month Post-Op","1 Month Post-Op", "3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","Single procedure anatomical Success", "6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","Final procedure anatomical Success","Final procedure anatomical Success"],
                                                            ["Database ID", "First Names' Letters", "DOB", "Age","Gender","Laterality (OD/OS)","Date","Fovea Status (Off / Split / On)","When did the shadow first appear? (in days)","When did the shadow first involved the central vision field? (in days)","Lens status (phakic/ pseudophakic/ aphakic)","Extent of the detachment (clock hours: hh:mm1-hh:mm2)","Main area of the detachment (sup/ inf/ total)","Number and Locations of retinal tears detached (number-clock hour, number-clock hour,.. )","Number and Locations of retinal tears attached (number-clock hour, number-clock hour,.. )","Size of the largest tear (optic disc measurment)","BCVA (snellen)","IOP (mmHg)","PVD status (Y/N)","PVR status (if yes, stage A/B/Ca/Cp)","Presence of vitreous hemorrhage (graded on a 5-point scale from 0 to 4)", "Date (dd/mm/yyyy)","Procedure type (PPV/ SB / PPV+SB)","Combined PhakoVitrectomy? (Y/N)","Cryo (Y/N)","Laser (number of pulses, energy (in mW), time (in seconds))","Drainage Technique (P- peripheral /R- retinotomy)","Tamponade used (Material, Volume)","PFO fluid (Y/N)","Number and Locations of retinal tears detached found Intra operativly (number-clock hour, number-clock hour,.. )", "Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)","Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)","Is there silicone oil in the eye?"]])
        #df.columns.values[0] = None
        #df = df.drop(df.index[0])
        #print(df.index[0])
        #print(df)
        #df = df.transpose()
        #print(df)
        for row in theposts:
            #print(row.dateofbirth)
            tuple_data = (row.id,row.firstandlast,row.dateofbirth,row.age,row.gender,row.laterality,row.date1,row.fovea_status,row.shadow,row.involved,row.lens_status,row.extent,row.area,row.detachedtotal,row.attachedtotal,row.size,row.bcva,row.iop,row.pvd,row.pvr,row.hemorrhage,row.date2,row.type,row.combined,row.cryo,row.laser,row.tech,row.tamp,row.pfo,row.found,row.date3,row.bcva2,row.iop2,row.date4,row.bcva3,row.iop3,row.date5,row.lens_status2,row.bcva4,row.iop4,row.m_charth,row.m_chartv,row.ask,row.questionnaire,row.acheive,row.date6,row.lens_status3,row.bcva5,row.iop5,row.m_charth2,row.m_chartv2,row.ask2,row.questionnaire2,row.date7,row.lens_status4,row.bcva6,row.iop6,row.m_charth3,row.m_chartv3,row.ask3,row.questionnaire3,row.acheive2, row.oil)
            newrow = pd.DataFrame([tuple_data],columns=[["Patient's Study Identifiers", "Patient's Study Identifiers", "Patient's Study Identifiers", "Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I","Pre-Op I", "Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II","Pre-Op II", "1 Week Post-Op","1 Week Post-Op","1 Week Post-Op","1 Month Post-Op","1 Month Post-Op","1 Month Post-Op", "3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","3 Month Post-Op","Single procedure anatomical Success", "6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","6 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","12 Month Post-Op","Final procedure anatomical Success","Final procedure anatomical Success"],["Database ID", "First Names' Letters", "DOB", "Age","Gender","Laterality (OD/OS)","Date","Fovea Status (Off / Split / On)","When did the shadow first appear? (in days)","When did the shadow first involved the central vision field? (in days)","Lens status (phakic/ pseudophakic/ aphakic)","Extent of the detachment (clock hours: hh:mm1-hh:mm2)","Main area of the detachment (sup/ inf/ total)","Number and Locations of retinal tears detached (number-clock hour, number-clock hour,.. )","Number and Locations of retinal tears attached (number-clock hour, number-clock hour,.. )","Size of the largest tear (optic disc measurment)","BCVA (snellen)","IOP (mmHg)","PVD status (Y/N)","PVR status (if yes, stage A/B/Ca/Cp)","Presence of vitreous hemorrhage (graded on a 5-point scale from 0 to 4)", "Date (dd/mm/yyyy)","Procedure type (PPV/ SB / PPV+SB)","Combined PhakoVitrectomy? (Y/N)","Cryo (Y/N)","Laser (number of pulses, energy (in mW), time (in seconds))","Drainage Technique (P- peripheral /R- retinotomy)","Tamponade used (Material, Volume)","PFO fluid (Y/N)","Number and Locations of retinal tears detached found Intra operativly (number-clock hour, number-clock hour,.. )", "Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)","Date (dd/mm/yyyy)","BCVA (snellen)","IOP (mmHg)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)", "Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Date (dd/mm/yyyy)","Lens status (phakic/ pseudophakic/ aphakic)","BCVA (snellen)","IOP (mmHg)","M-CHART MH score","M-CHART MV score","ASK (measurment)","M-Questionnaire","Did the first surgery achieved reattchment (Y/N)","Is there silicone oil in the eye?"]])
        
            df = pd.concat([df,newrow], ignore_index=True)
            #print(df)
            #newrow = newrow.transpose()
            #print(newrow)
        #print(type(row))

        #df = pd.DataFrame([row.__dict__ for row in theposts])
        #column_1 = df.iloc[:, 1]
        #print(column_1)
        #df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1])
        df.to_excel('data.xlsx')
        return render_template("allpatients.html",user = user, theposts=theposts)

#Full screen all patient table
@app.route('/fullscreen/<int:user>', methods=['GET', 'POST'])
@login_required
def fullscreen(user):
    if current_user.id == 1:
        user = 1
        theposts = Posts.query.all()
        return render_template("fullscreen.html",user = user, theposts=theposts)

    elif user == current_user.id:
    
        theposts = Posts.query.filter_by(poster_id = user)
        return render_template("fullscreen.html",user = user, theposts=theposts)



    
# Returning data to user in excel format
@app.route("/return-file/<int:user>", methods=["GET", "POST"])
@login_required
def return_file(user):
    if user == current_user.id:
        return send_file("data.xlsx")

@app.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    if current_user.id == 1:
        post = Posts.query.get_or_404(id)
        user = 1
        s_id = post.id
        return render_template("profile.html", s_id = s_id, post=post, id = id, user=user)
    else:

        post = Posts.query.get_or_404(id)
        user = current_user.id
        if post.poster_id == current_user.id:
        
            s_id = post.id
    
    return render_template("profile.html", s_id = s_id, post=post, id = id, user=user)


@app.route('/preop1/<int:id>', methods=['GET', 'POST'])
@login_required
def preop1(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id
    form = PostForm()
    if form.validate_on_submit():
            emptycheckdetached = [form.detached.data, form.detached2.data, form.detached3.data, form.detached4.data, form.detached5.data] 
            filtered_variables = [str(detached) for detached in emptycheckdetached if detached is not None]   
            detachedtotal = ' '.join(filtered_variables)

            emptycheckattached = [form.attached.data, form.attached2.data, form.attached3.data, form.attached4.data, form.attached5.data] 
            filtered_variables = [str(attached) for attached in emptycheckattached if attached is not None]   
            attachedtotal = ' '.join(filtered_variables)
        #thepost.author = form.author.data
            thepost.age = form.age.data
            thepost.gender = form.gender.data
            thepost.dateofbirth = form.dateofbirth.data
            thepost.firstandlast = form.firstandlast.data
            thepost.laterality = form.laterality.data
            thepost.date1 = form.date1.data
            thepost.fovea_status = form.fovea_status.data
            thepost.shadow=form.shadow.data
            thepost.involved=form.involved.data
            thepost.lens_status=form.lens_status.data
            thepost.extent=form.extent.data
            thepost.area=form.area.data
            thepost.detached=form.detached.data
            thepost.detached2=form.detached2.data
            thepost.detached3=form.detached3.data
            thepost.detached4=form.detached4.data
            thepost.detached5=form.detached5.data
            thepost.detachedtotal=detachedtotal
            thepost.attached=form.attached.data
            thepost.attached2=form.attached2.data
            thepost.attached3=form.attached3.data
            thepost.attached4=form.attached4.data
            thepost.attached5=form.attached5.data
            thepost.attachedtotal=attachedtotal
            thepost.size=form.size.data
            thepost.bcva=form.bcva.data
            thepost.iop=form.iop.data
            thepost.pvd=form.pvd.data
            thepost.pvr=form.pvr.data
            thepost.hemorrhage=form.hemorrhage.data

            # Update Database
            db.session.add(thepost)
            db.session.commit()

            # message
            flash("Patient data has been updated!")

            return redirect(url_for('preop1', id=thepost.id))
    if thepost.poster_id == current_user.id or current_user.id == 1:
        #Upload to s3 bucket and update oct class in local db                                                                                                    
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 1)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 1)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=60
                    )
                    #print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)

        form.age.data = thepost.age
        form.gender.data = thepost.gender
        form.dateofbirth.data = thepost.dateofbirth
        form.firstandlast.data = thepost.firstandlast
        form.laterality.data = thepost.laterality
        form.date1.data = thepost.date1
        form.fovea_status.data = thepost.fovea_status
        form.shadow.data = thepost.shadow
        form.involved.data = thepost.involved
        form.lens_status.data = thepost.lens_status
        form.extent.data = thepost.extent
        form.area.data = thepost.area
        form.detached.data = thepost.detached
        form.detached2.data = thepost.detached2
        form.detached3.data = thepost.detached3
        form.detached4.data = thepost.detached4
        form.detached5.data = thepost.detached5
        form.attached.data = thepost.attached
        form.attached2.data = thepost.attached2
        form.attached3.data = thepost.attached3
        form.attached4.data = thepost.attached4
        form.attached5.data = thepost.attached5
        form.size.data = thepost.size
        form.bcva.data = thepost.bcva
        form.iop.data = thepost.iop
        form.pvd.data = thepost.pvd
        form.pvr.data = thepost.pvr
        form.hemorrhage.data = thepost.hemorrhage
        
    return render_template("preop1.html", s_id = s_id, profile = thepost, id = id, list = list, form = form, user=poster)

@app.route('/preop2/<int:id>', methods=['GET', 'POST'])
@login_required
def preop2(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id
    form = UpdateForm()
    if form.validate_on_submit():
        emptycheckfound = [form.found.data, form.found2.data, form.found3.data, form.found4.data, form.found5.data] 
        filtered_variables = [str(found) for found in emptycheckfound if found is not None]   
        foundtotal = ' '.join(filtered_variables)

        thepost.date2=form.date2.data
        thepost.type=form.type.data
        thepost.combined=form.combined.data
        thepost.cryo=form.cryo.data
        thepost.laser=form.laser.data
        thepost.tech=form.tech.data
        thepost.tamp=form.tamp.data
        thepost.pfo=form.pfo.data
        thepost.found=form.found.data
        thepost.found2=form.found2.data
        thepost.found3=form.found3.data
        thepost.found4=form.found4.data
        thepost.found5=form.found5.data
        thepost.foundtotal=foundtotal
        # Update Database
        db.session.add(thepost)
        db.session.commit()

        # message
        flash("Patient data has been updated!")

        return redirect(url_for('preop2', id=thepost.id))
    
    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 2)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 2)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=60
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)

        form.date2.data = thepost.date2
        form.type.data = thepost.type
        form.combined.data = thepost.combined
        form.cryo.data = thepost.cryo
        form.laser.data = thepost.laser
        form.tech.data = thepost.tech
        form.tamp.data = thepost.tamp
        form.pfo.data = thepost.pfo
        form.found.data = thepost.found
        form.found2.data = thepost.found2
        form.found3.data = thepost.found3
        form.found4.data = thepost.found4
        form.found5.data = thepost.found5
    return render_template("preop2.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)



@app.route('/postop1/<int:id>', methods=['GET', 'POST'])
@login_required
def postop1(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id
    
    form = UpdateForm()
    if form.validate_on_submit():

            thepost.date3=form.date3.data
            thepost.bcva2=form.bcva2.data
            thepost.iop2=form.iop2.data
            # Update Database
            db.session.add(thepost)
            db.session.commit()

            # message
            flash("Patient data has been updated!")

            return redirect(url_for('postop1', id=thepost.id))

    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 3)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 3)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=3600
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)
        form.date3.data = thepost.date3
        form.bcva2.data = thepost.bcva2
        form.iop2.data = thepost.iop2
    return render_template("postop1.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)

@app.route('/postop2/<int:id>', methods=['GET', 'POST'])
@login_required
def postop2(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id

    form = UpdateForm()
    if form.validate_on_submit():

            thepost.date4=form.date4.data
            thepost.bcva3=form.bcva3.data
            thepost.iop3=form.iop3.data
            # Update Database
            db.session.add(thepost)
            db.session.commit()

            # message
            flash("Patient data has been updated!")

            return redirect(url_for('postop2', id=thepost.id))

    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 4)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 4)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=3600
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)
        form.date4.data = thepost.date4
        form.bcva3.data = thepost.bcva3
        form.iop3.data = thepost.iop3
    return render_template("postop2.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)
@app.route('/postop3/<int:id>', methods=['GET', 'POST'])
@login_required
def postop3(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id

    
    form = UpdateForm()
    if form.validate_on_submit():

        thepost.date5=form.date5.data
        thepost.lens_status2=form.lens_status2.data
        thepost.bcva4=form.bcva4.data
        thepost.iop4=form.iop4.data
        thepost.m_charth=form.m_charth.data
        thepost.m_chartv=form.m_chartv.data
        thepost.ask=form.ask.data
        thepost.questionnaire=form.questionnaire.data
        thepost.acheive=form.acheive.data
            # Update Database
        db.session.add(thepost)
        db.session.commit()

            # message
        flash("Patient data has been updated!")

        return redirect(url_for('postop3', id=thepost.id))

    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 5)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 5)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=3600
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)
        form.date5.data = thepost.date5
        form.lens_status2.data = thepost.lens_status2
        form.bcva4.data = thepost.bcva4
        form.iop4.data = thepost.iop4
        form.m_charth.data = thepost.m_charth
        form.m_chartv.data = thepost.m_chartv
        form.ask.data = thepost.ask
        form.questionnaire.data = thepost.questionnaire
        form.acheive.data = thepost.acheive
    return render_template("postop3.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)
@app.route('/postop4/<int:id>', methods=['GET', 'POST'])
@login_required
def postop4(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id
        
    form = UpdateForm()
    if form.validate_on_submit():

        thepost.date6=form.date6.data
        thepost.lens_status3=form.lens_status3.data
        thepost.bcva5=form.bcva5.data
        thepost.iop5=form.iop5.data
        thepost.m_charth2=form.m_charth2.data
        thepost.m_chartv2=form.m_chartv2.data
        thepost.ask2=form.ask2.data
        thepost.questionnaire2=form.questionnaire2.data
            # Update Database
        db.session.add(thepost)
        db.session.commit()

            # message
        flash("Patient data has been updated!")

        return redirect(url_for('postop4', id=thepost.id))

    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 6)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 6)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=3600
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)
        form.date6.data = thepost.date6
        form.lens_status3.data = thepost.lens_status3
        form.bcva5.data = thepost.bcva5
        form.iop5.data = thepost.iop5
        form.m_charth2.data = thepost.m_charth2
        form.m_chartv2.data = thepost.m_chartv2
        form.ask2.data = thepost.ask2
        form.questionnaire2.data = thepost.questionnaire2
    return render_template("postop4.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)
@app.route('/postop5/<int:id>', methods=['GET', 'POST'])
@login_required
def postop5(id):

    thepost = Posts.query.get_or_404(id)
    s_id = thepost.id

    poster = thepost.poster_id
            
    form = UpdateForm()
    if form.validate_on_submit():

        thepost.date7=form.date7.data
        thepost.lens_status4=form.lens_status4.data
        thepost.bcva6=form.bcva6.data
        thepost.iop6=form.iop6.data
        thepost.m_charth3=form.m_charth3.data
        thepost.m_chartv3=form.m_chartv3.data
        thepost.ask3=form.ask3.data
        thepost.questionnaire3=form.questionnaire3.data
        thepost.acheive2=form.acheive.data
        thepost.oil=form.oil.data
            # Update Database
        db.session.add(thepost)
        db.session.commit()

            # message
        flash("Patient data has been updated!")

        return redirect(url_for('postop5', id=thepost.id))

    if thepost.poster_id == current_user.id or current_user.id == 1:
                                                                                                            
        if request.method == 'POST':
            if request.files:
                files = request.files["Upload"]
                if files:
                    files = request.files.getlist("Upload") 
                    for file in files:   
                        post_id = thepost.id
                        
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 7)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                        
                        flash("OCT image data was uploaded successfully")

        list = []
        #vcregion = s3_client.meta.region_name
    
        
        #print('Client region:', region)
        theocts = Octs.query.filter_by(post_id = s_id, op = 7)
        objects = s3_client.list_objects(Bucket='test')
        for i in theocts:
            #print(type(i.filename))
            for obj in objects['Contents']:
            #    print(type(obj['Key']))
                if obj['Key'] == i.filename:

                    #try:
                    response = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': 'test', 'Key': obj['Key']},
                    ExpiresIn=3600
                    )
                    print('Pre-signed URL:', response)
                    #except:
                    #    print('Error')
                    list.append(response)
                    #print("yes")
                    # print(obj['Key'])
                    # print(i.filename)
        #print(list)
        form.date7.data = thepost.date7
        form.lens_status4.data = thepost.lens_status4
        form.bcva6.data = thepost.bcva6
        form.iop6.data = thepost.iop6
        form.m_charth3.data = thepost.m_charth3
        form.m_chartv3.data = thepost.m_chartv3
        form.ask3.data = thepost.ask3
        form.questionnaire3.data = thepost.questionnaire3
        form.acheive.data = thepost.acheive2
        form.oil.data = thepost.oil
    return render_template("postop5.html", s_id = s_id, profile = thepost, id = id, list = list, user=poster, form=form)

@app.route('/add-post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        
        poster = current_user.id

        # emptycheck = [form.extent.data, form.extent2.data, form.extent3.data, form.extent4.data, form.extent5.data] 
        # filtered_variables = [str(extent) for extent in emptycheck if extent is not None]   
        # extenttotal = ' '.join(filtered_variables)


        emptycheckdetached = [form.detached.data, form.detached2.data, form.detached3.data, form.detached4.data, form.detached5.data] 
        filtered_variables = [str(detached) for detached in emptycheckdetached if detached is not None]   
        detachedtotal = ' '.join(filtered_variables)

        emptycheckattached = [form.attached.data, form.attached2.data, form.attached3.data, form.attached4.data, form.attached5.data] 
        filtered_variables = [str(attached) for attached in emptycheckattached if attached is not None]   
        attachedtotal = ' '.join(filtered_variables)

        emptycheckfound = [form.found.data, form.found2.data, form.found3.data, form.found4.data, form.found5.data] 
        filtered_variables = [str(found) for found in emptycheckfound if found is not None]   
        foundtotal = ' '.join(filtered_variables)
       
        post = Posts(age=form.age.data, poster_id = poster, gender=form.gender.data, dateofbirth=form.dateofbirth.data, firstandlast=form.firstandlast.data, laterality = form.laterality.data, date1 = form.date1.data, fovea_status = form.fovea_status.data,  shadow=form.shadow.data, involved=form.involved.data,
                        lens_status=form.lens_status.data, extent=form.extent.data, area=form.area.data, detached=form.detached.data,detached2=form.detached2.data,detached3=form.detached3.data,detached4=form.detached4.data,detached5=form.detached5.data,detachedtotal=detachedtotal,attached=form.attached.data,attached2=form.attached2.data,attached3=form.attached3.data,attached4=form.attached4.data,attached5=form.attached5.data,attachedtotal=attachedtotal, size=form.size.data, bcva=form.bcva.data, iop=form.iop.data, pvd=form.pvd.data, pvr=form.pvr.data, hemorrhage=form.hemorrhage.data, date2=form.date2.data, type=form.type.data,
                        combined=form.combined.data, cryo=form.cryo.data, laser=form.laser.data, tech=form.tech.data, tamp=form.tamp.data, pfo=form.pfo.data, found =form.found.data,found2 =form.found2.data,found3 =form.found3.data,found4 =form.found4.data,found5 =form.found5.data,foundtotal=foundtotal, date3=form.date3.data, bcva2=form.bcva2.data, iop2=form.iop2.data, date4=form.date4.data, bcva3=form.bcva3.data, iop3=form.iop3.data,
                            date5=form.date5.data, lens_status2=form.lens_status2.data, bcva4=form.bcva4.data, iop4=form.iop4.data, m_charth=form.m_charth.data, m_chartv=form.m_chartv.data, ask=form.ask.data, questionnaire=form.questionnaire.data,
                            date6=form.date6.data, lens_status3=form.lens_status3.data, bcva5=form.bcva5.data, iop5=form.iop5.data, m_charth2=form.m_charth2.data, m_chartv2=form.m_chartv2.data, ask2=form.ask2.data, questionnaire2=form.questionnaire2.data,
                            date7=form.date7.data, lens_status4=form.lens_status4.data, bcva6=form.bcva6.data, iop6=form.iop6.data, m_charth3=form.m_charth3.data, m_chartv3=form.m_chartv3.data, ask3=form.ask3.data, questionnaire3=form.questionnaire3.data, acheive2=form.acheive2.data,acheive=form.acheive.data, oil=form.oil.data)
        db.session.add(post)
        db.session.commit()
        #return a message
        flash("Patient Profile Created Successfully! You may view your patient in the Overview tab and upload your patient's OCTs by pressing their Database ID.")
        post_id = post.id

        if request.files:
            files = request.files["Upload"]
            if files:
                files = request.files.getlist("Upload")
                for file in files:
                    file.filename = make_unique(file.filename)
                    oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 1)
                    db.session.add(oct)
                    db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                    s3.upload_fileobj(file,'test', file.filename)

                files = request.files["Upload2"]
                if files:
                    files = request.files.getlist("Upload2")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 2)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)       

                files = request.files["Upload3"]
                if files:
                    files = request.files.getlist("Upload3")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 3)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                
                files = request.files["Upload4"]
                if files:
                    files = request.files.getlist("Upload4")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 4)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)
                
                files = request.files["Upload5"]
                if files:
                    files = request.files.getlist("Upload5")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 5)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)                                                     
                        
                files = request.files["Upload6"]
                if files:
                    files = request.files.getlist("Upload6")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 6)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)    

                        
                files = request.files["Upload7"]
                if files:
                    files = request.files.getlist("Upload7")
                    for file in files:
                        file.filename = make_unique(file.filename)
                        oct = Octs(filename = file.filename, poster_id = poster, post_id = post_id, op = 7)
                        db.session.add(oct)
                        db.session.commit()
                        #flash("OCT metadata Uploaded successfully")
                        s3.upload_fileobj(file,'test', file.filename)    
            flash("OCT image data was uploaded successfully")

        return redirect(url_for("allpatients", user = poster))

    else:
        poster = current_user.id

        flash("No Patient Added")

    #redirect 
    return render_template("add_post.html", form = form)

@app.route('/deletewarning/<int:id>', methods=['GET', 'POST'])
@login_required
def deletewarning(id):
    if current_user.id == 1:
        id=id
        return render_template("deletewarning.html", id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    if current_user.id == 1:
         
        post_to_delete = Posts.query.get_or_404(id)

        try:
            db.session.delete(post_to_delete)
            db.session.commit()

            # return a message
            flash("Post was deleted")

            return redirect(url_for("allpatients", user = current_user.id))

        except:

            flash("Whoops, there was an error")

            return redirect(url_for("allpatients", user = current_user.id))

#add a user
@app.route('/user/add', methods=['Get','Post'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            # Hash the password first
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")

            user = Users(name=form.name.data, username = form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("User added, you may now login")
            name = form.name.data
        else: 
            flash("Username already in use. Please choose a different username")
        form.name.data=''
        form.email.data=''
        form.favorite_color.data=''
        form.password_hash.data = ''
        form.username.data = ''
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form = form, name = name, our_users=our_users)
# edit user password
@app.route('/password', methods=['Get','Post'])
@login_required
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        userid = current_user.id
        user = Users.query.filter_by(id=userid).first()

        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user.password_hash = hashed_pw
        db.session.commit()
        flash("Password changed")

        return redirect(url_for("dashboard", user = current_user.id))
    else:
        flash("Password not changed")
    form.password_hash.data = ''
    form.password_hash2.data = ''
    return render_template("password.html", form = form)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500



# CLASSES

# Create a post model for our database 


# flask db migrate -m 'added foreign key'
# flask db upgrade
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateofbirth = db.Column(db.Date)
    firstandlast = db.Column(db.String(10))
    age = db.Column(db.String(4))
    gender = db.Column(db.String(10))
    laterality = db.Column(db.String(10))
    date1 = db.Column(db.Date)
    fovea_status=db.Column(db.String(255))
    shadow = db.Column(db.String(255))
    involved = db.Column(db.String(255))
    lens_status = db.Column(db.String(255))
    extent = db.Column(db.String(255))
    extent2 = db.Column(db.String(255))
    extent3 = db.Column(db.String(255))
    extent4 = db.Column(db.String(255))
    extent5 = db.Column(db.String(255))    
    extenttotal = db.Column(db.String(255))    
    area = db.Column(db.String(255))
    detached = db.Column(db.String(255))
    detached2 = db.Column(db.String(255))
    detached3 = db.Column(db.String(255))
    detached4 = db.Column(db.String(255))
    detached5 = db.Column(db.String(255))
    detachedtotal = db.Column(db.String(255))
    attached = db.Column(db.String(255))
    attached2 = db.Column(db.String(255))
    attached3 = db.Column(db.String(255))
    attached4 = db.Column(db.String(255))
    attached5 = db.Column(db.String(255))
    attachedtotal = db.Column(db.String(255))
    size = db.Column(db.String(255)) 
    bcva = db.Column(db.String(255))
    iop = db.Column(db.Float(25))
    pvd = db.Column(db.String(255))
    pvr = db.Column(db.String(255))
    hemorrhage = db.Column(db.String(255))
    date2 = db.Column(db.Date)
    type = db.Column(db.String(255))
    combined = db.Column(db.String(255))
    cryo = db.Column(db.String(255))
    laser = db.Column(db.String(255))
    tech = db.Column(db.String(255))
    tamp = db.Column(db.String(255))
    tampv = db.Column(db.Float(25))
    tampt = db.Column(db.String(255))
    pfo = db.Column(db.String(255))
    found = db.Column(db.String(255))
    found2 = db.Column(db.String(255))
    found3 = db.Column(db.String(255))
    found4 = db.Column(db.String(255))
    found5 = db.Column(db.String(255))
    foundtotal = db.Column(db.String(255))
    acheive = db.Column(db.String(255))
    date3 = db.Column(db.Date)
    bcva2 = db.Column(db.String(255))
    iop2 = db.Column(db.Float(25))
    date4 = db.Column(db.Date)
    bcva3 = db.Column(db.String(255))
    iop3 = db.Column(db.Float(25))
    date5 = db.Column(db.Date)
    lens_status2 = db.Column(db.String(255))
    bcva4 = db.Column(db.String(255))
    iop4 = db.Column(db.Float(25))
    m_charth = db.Column(db.Float(25))
    m_chartv = db.Column(db.Float(25))
    ask = db.Column(db.Float(25))
    questionnaire = db.Column(db.String(255))
    date6 = db.Column(db.Date)
    lens_status3 = db.Column(db.String(255))
    bcva5 = db.Column(db.String(255))
    iop5 = db.Column(db.Float(25))
    m_charth2 = db.Column(db.Float(25))
    m_chartv2 = db.Column(db.Float(25))
    ask2 = db.Column(db.Float(25))
    questionnaire2 = db.Column(db.Float(25))
    date7 = db.Column(db.Date)
    lens_status4 = db.Column(db.String(255))
    bcva6 = db.Column(db.String(255))
    iop6 = db.Column(db.Float(25))
    m_charth3 = db.Column(db.Float(25))
    m_chartv3 = db.Column(db.Float(25))
    ask3 = db.Column(db.Float(25))
    questionnaire3 = db.Column(db.Float(25))
    acheive2 = db.Column(db.String(255))
    oil = db.Column(db.String(255))
    #author = db.Column(db.String(255))
    
    # Foreign Key to link users (refer to primary key of the user)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    octs = db.relationship('Octs', backref='octpost')
# OCTS Model4
class Octs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer(), db.ForeignKey('posts.id'))
    op = db.Column(db.Integer())

# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=True)
	email = db.Column(db.String(120), nullable=True, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(), nullable=True)
	# Do some password stuff!
	password_hash = db.Column(db.String(128))
	# User Can Have Many Posts 
	posts = db.relationship('Posts', backref='poster')


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute!')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.name


#heroku git:remote -a your-heroku-app-name