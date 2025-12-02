from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class PatientForm(FlaskForm):
    patient_id = StringField("Patient ID", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("Male","Male"),("Female","Female"),("Other","Other")])
    age = IntegerField("Age", validators=[DataRequired()])
    hypertension = SelectField("Hypertension", choices=[("0","No"),("1","Yes")])
    ever_married = SelectField("Ever Married", choices=[("No","No"),("Yes","Yes")])
    work_type = SelectField("Work Type", choices=[
        ("Children","Children"),("Govt_job","Govt_job"),("Never_worked","Never_worked"),
        ("Private","Private"),("Self-employed","Self-employed")
    ])
    residence_type = SelectField("Residence Type", choices=[("Urban","Urban"),("Rural","Rural")])
    avg_glucose_level = FloatField("Avg. Glucose Level", validators=[DataRequired()])
    bmi = FloatField("BMI", validators=[DataRequired()])
    smoking_status = SelectField("Smoking Status", choices=[
        ("Formerly smoked","Formerly smoked"),("Never smoked","Never smoked"),
        ("Smokes","Smokes"),("Unknown","Unknown")
    ])
    stroke = SelectField("Stroke", choices=[("0","No"),("1","Yes")])
    submit = SubmitField("Submit")
