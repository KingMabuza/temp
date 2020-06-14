from __future__ import print_function
from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from flask_material import Material
from pymongo import MongoClient
from contact_form import ContactForm, NewsletterForm
import smtplib
from email.message import EmailMessage
import requests
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

app = Flask(__name__)
mail = Mail(app)
Material(app)

app.config['SECRET_KEY'] = 'faabcdf49810c0f43a9da9763e90f392'

cluster = MongoClient('mongodb://localhost:27017')
db = cluster["NastyC"]
collection = db["Events"]

# post = {"_id": 3, "name": "Back To The City", "Date": "3 July 2020", "city": "Johannesburg"}
# collection.insert_one(post)

doc = db["emails"]

# sendinblue
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key[
    'fornasty'] = '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'
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['partner-key'] = 'F5XqJvUaNTbdn36H'


@app.route('/')
@app.route('/home')
def home():
    return render_template('main.html')


@app.route('/music', methods=["GET", "POST"])
def music():
    newsletterForm = NewsletterForm()

    return render_template('albums.html', newsletterForm=newsletterForm)


@app.route('/tour', methods=['GET', 'POST'])
def tour():
    e = collection.find()
    newsletterForm = NewsletterForm()
    return render_template('tour.html', e=e, newsletterForm=newsletterForm)


@app.route('/contact', methods=["GET", "POST"])
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    if request.method == "POST":
        req = request.form
        name = req["name"]
        email = req["emailaddress"]

        post = {"name": name, "email": email}
        doc.insert_one(post)

        api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
        create_contact = sib_api_v3_sdk.CreateContact(email)

        try:
            # Create a contact
            api_response = api_instance.create_contact(create_contact)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ContactsApi->create_contact: %s\n" % e)

    return render_template('subscribe.html')


@app.route('/sent', methods=["GET", "POST"])
def sent():
    if request.method == "POST":

        with smtplib.SMTP_SSL('smtp-relay.sendinblue.com', 465) as smtp:
            smtp.login('Amal@amallevi.com', 'xsmtpsib-d5753337cbdfe8bb06dfdfdf0db650834205140277c3d7dafcbdf0b88864c76e'
                                            '-s57vz2nEQPp3NaqA')
            req = request.form
            firstname = req["firstName"]
            lastname = req["lastName"]
            email = req["email"]
            telephone = req["telephone"]
            organisation = req["organisation"]
            city = req["city"]
            country = req["country"]
            purpose = req["purpose"]
            message = req["message"]
            send = f''' First Name: {firstname} 
                        Last Name: {lastname} 
                        Telephone: {telephone} 
                        Organisation: {organisation}  
                        City: {city} 
                        Country:{country} 
                        Message:{message}'''
            msg = EmailMessage()
            msg['Subject'] = purpose
            msg['From'] = email
            msg['To'] = 'amal@amallevi.com'
            msg.set_content(send)
            smtp.send_message(msg)

    return render_template('sent.html')


if __name__ == '__main__':
    app.run()
