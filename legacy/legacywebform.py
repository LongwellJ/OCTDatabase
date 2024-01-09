from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, DateField, RadioField, IntegerField, DecimalField, FieldList
from wtforms.validators import DataRequired, EqualTo, Length, optional, NumberRange, Regexp
from wtforms_components import TimeField
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

# Create A Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")
        
# DOB form 
class DobForm(FlaskForm):
    dateofbirth = DateField("Date of Birth", validators=[DataRequired()])
    firstandlast = StringField("Initial of First and Last Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class IDForm(FlaskForm):
    dateofbirth = DateField("Date of Birth", validators=[DataRequired()])
    firstandlast = StringField("Initial of First and Last Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")


#Form for Posts
class PostForm(FlaskForm):
    age=IntegerField("Age", validators=[optional(), NumberRange(min=1, max=999, message='Invalid length')])
    gender=RadioField("Gender", choices=["Female", "Male"], validators=[optional()])
    dateofbirth = DateField("Date of Birth", validators=[DataRequired()])
    firstandlast = StringField("Initial of First and Last Name", validators=[DataRequired()])
    laterality=RadioField("Laterality", choices=["OD", "OS"], validators=[optional()])
    date1 = DateField("Date", validators=[optional()])
    fovea_status=RadioField("Fovea Status", choices=["Off", "Split", "On"], validators=[optional()])
    shadow =IntegerField("When did the shadow first appear? (in days)",validators=[optional(), NumberRange(min=1, max=9999, message='Invalid length')])
    involved =IntegerField("When did the shadow first involve the central vision field? (in days)",validators=[optional(),NumberRange(min=1, max=9999, message='Invalid length')])
    lens_status=RadioField("Lens status",choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    extent = StringField("Extent of the detachment clockwise (hh:mm-hh:mm)", validators=[optional(), Regexp(r'^([01]?[0-9]|2[0-3]):[0-5][0-9]-([01]?[0-9]|2[0-3]):[0-5][0-9]$', message="must be in the format hh:mm-hh:mm where h and m are numbers.")])
    area =RadioField("Main area of the detachment",choices=["Superior", "Inferior", "Superior & Inferior"], validators=[optional()])
    detached =StringField("Number and Locations of retinal tears DETACHED (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    detached2 =StringField("Number and Locations of retinal tears DETACHED (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    detached3 =StringField("Number and Locations of retinal tears DETACHED (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    detached4 =StringField("Number and Locations of retinal tears DETACHED (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    detached5 =StringField("Number and Locations of retinal tears DETACHED (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    attached =StringField("Number and Locations of retinal tears ATTACHED  (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    attached2 =StringField("Number and Locations of retinal tears ATTACHED  (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    attached3 =StringField("Number and Locations of retinal tears ATTACHED  (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    attached4 =StringField("Number and Locations of retinal tears ATTACHED  (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    attached5 =StringField("Number and Locations of retinal tears ATTACHED  (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    size =RadioField("Size of the largest tear in clock hours (optic disc measurment)",choices=["1/4", "1/2", "1", "2", "3", ">3"], validators=[optional()])
    bcva =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop=DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    pvd=RadioField("PVD status", choices=["Yes", "No"], validators=[optional()])
    pvr =RadioField("PVR status ",choices=["A (Vitreous haze, pigment clumps)", "B (Inner retinal wrinkling, rolled edge of breaks)", "Ca (Traction in anterior retina)", "Cp (Contraction or subretinal membrane in posterior retina)","No PVR"], validators=[optional()])
    hemorrhage =RadioField("Presence of vitreous hemorrhage",choices=["0 (No vitreous hemorrhage )", "1 (Mild vitreous hemorrhage- visible fundus details)", "2 (Moderate vitreous hemorrhage- No visible fundus details, orange reflex exist) ", "3 ( Severe vitreous hemorrhage- No visible fundus details, No orange reflex) "], validators=[optional()])
    date2 = DateField("Date", validators=[optional()])
    type =RadioField("Procedure type",choices=["PPV", "SB", "PPV+SB"], validators=[optional()])
    combined =RadioField("Combined PhakoVitrectomy?",choices=["Yes", "No"], validators=[optional()])
    cryo =RadioField("Cryo",choices=["Yes", "No"], validators=[optional()])
    laser =StringField("Laser:number of pulses-energy in mW-time in seconds(nn-nnn-nn)", validators=[optional(), Regexp(r'^\d{2}-\d{3}-\d{2}', message="must be in the format nn-nnn-nn where n is a digit.")])
    tech =RadioField("Drainage Technique",choices=["Peripheral break", "Posterior retinotomy"], validators=[optional()])
    tamp =StringField("Tamponade Material", validators=[optional()])
    pfo =RadioField("PFO fluid",choices=["Yes", "No"], validators=[optional()])
    found =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found2 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found3 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found4 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found5 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    acheive =RadioField("Did the first surgery achieve reattchment",choices=["Yes", "No"], validators=[optional()])
    date3 = DateField("Date", validators=[optional()])
    bcva2 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop2 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    date4 = DateField("Date", validators=[optional()])
    bcva3 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop3 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    date5 = DateField("Date", validators=[optional()])
    lens_status2 =RadioField("Lens status",choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva4 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop4 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth=DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    date6 = DateField("Date", validators=[optional()])
    lens_status3 =RadioField("Lens status",choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva5 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop5 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth2 =DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv2 =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask2 =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire2 =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    date7 = DateField("Date", validators=[optional()])
    lens_status4 =RadioField("Lens status", choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva6 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop6 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth3 =DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv3 =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask3 =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire3 =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    acheive2 =RadioField("Final procedure anatomical success",choices=["Yes", "No"], validators=[optional()])    
    oil = RadioField("Is there silicone oil in the eye?", choices=["Yes", "No"], validators=[optional()])
    submit=SubmitField("Submit")



#Form for updating Posts without the dateofbirth because it is considered nessesary to create a new patient in the addpost
class UpdateForm(FlaskForm):
    date2 = DateField("Date", validators=[optional()])
    type =RadioField("Procedure type",choices=["PPV", "SB", "PPV+SB"], validators=[optional()])
    combined =RadioField("Combined PhakoVitrectomy?",choices=["Yes", "No"], validators=[optional()])
    cryo =RadioField("Cryo",choices=["Yes", "No"], validators=[optional()])
    laser =StringField("Laser:number of pulses-energy in mW-time in seconds(nn-nnn-nn)", validators=[optional(), Regexp(r'^\d{2}-\d{3}-\d{2}', message="must be in the format nn-nnn-nn where n is a digit.")])
    tech =RadioField("Drainage Technique",choices=["Peripheral", "Retinotomy"], validators=[optional()])
    tamp =StringField("Tamponade Material", validators=[optional()])
    pfo =RadioField("PFO fluid",choices=["Yes", "No"], validators=[optional()])
    found =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found2 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found3 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found4 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    found5 =StringField("Number and Locations of retinal tears detached found Intra operativly (number-hh:mm)", validators=[optional(), Regexp(r'\d+-([01]\d|2[0-3]):[0-5]\d', message="must be in the format number-hh:mm where number is one digit and h and m are numbers.")])
    acheive =RadioField("Did the first surgery achieve reattchment",choices=["Yes", "No"], validators=[optional()])
    date3 = DateField("Date", validators=[optional()])
    bcva2 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop2 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    date4 = DateField("Date", validators=[optional()])
    bcva3 =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop3 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    date5 = DateField("Date", validators=[optional()])
    lens_status2 =RadioField("Lens status",choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva4  =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop4 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth=DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    date6 = DateField("Date", validators=[optional()])
    lens_status3 =RadioField("Lens status",choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva5  =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop5 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth2 =DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv2 =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask2 =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire2 =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    date7 = DateField("Date", validators=[optional()])
    lens_status4 =RadioField("Lens status", choices=["Phakic", "Pseudophakic", "Aphakic"], validators=[optional()])
    bcva6  =StringField("BCVA (snellen), for non-numerical values please use one of the following: CF/HM/LP/NLP",validators=[optional(), Regexp(r'^\d{2}\/\d{2}$', message="BCVA must be in the format XX/XX where X is a digit.")])
    iop6 =DecimalField("IOP (mmHg)", validators=[optional()], places=2)
    m_charth3 =DecimalField("M-CHART MH score", validators=[optional()], places=2)
    m_chartv3 =DecimalField("M-CHART MV score", validators=[optional()], places=2)
    ask3 =DecimalField("ASK (measurment)", validators=[optional()], places=2)
    questionnaire3 =DecimalField("M-Questionnaire score", validators=[optional()], places=2)
    acheive2 =RadioField("Did the first surgery achieve reattchment",choices=["Yes", "No"], validators=[optional()])
    oil = RadioField("Is there silicone oil in the eye?", choices=["Yes", "No"], validators=[optional()])

    
    submit=SubmitField("Submit")
# Form for registration
class UserForm(FlaskForm):
    name = StringField("Name", validators=[optional()])
    username = StringField("Username", validators=[DataRequired()])
    #profile_pic = FileField("Update Profile Pic") 
    email = StringField("Email", validators=[optional()])
    favorite_color = StringField("Favorite color")
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


# Form for password checking
class PasswordForm(FlaskForm):
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])

    submit = SubmitField("Submit")

    # Check docs for all the form types
    #Flask WTF
