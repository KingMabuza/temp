from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, SelectField
from wtforms.fields.html5 import TelField, EmailField


class ContactForm(FlaskForm):
    firstName = StringField("firstName", [validators.required("Please Enter A First Name ")])
    lastName = StringField("lastName", [validators.required("Please Enter A LAst Name")])
    email = EmailField("email", [validators.required("Please Enter An Email Address")])
    telephone = TelField("telephone", [validators.required("Please Enter A Telephone Number")])
    organisation = StringField("organisation", [validators.required("Please Enter An Organisation Name")])
    city = StringField("city", [validators.required("Please Enter A City")])
    country = StringField("country", [validators.required("Please Enter A Country")])
    purpose = SelectField("purpose", [validators.required("Please Select A Purpose")], choices=[("Booking", "Booking"), ("Media", "Media"), ("Other", "Other")])
    message = StringField("message", [validators.required("Please Enter A Message")])
    submit = SubmitField("submit")


class NewsletterForm(FlaskForm):
    name = StringField("name", [validators.required()])
    emailaddress = EmailField("emailaddress", [validators.required()])
    submit = SubmitField("submit")
