from flask import Flask, render_template, request, url_for, redirect, flash, current_app
from . import app
from .forms import ContactForm
import logging
import os

logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(os.path.abspath(logs_dir), exist_ok=True)
logging.basicConfig(
    filename=os.path.join(os.path.abspath(logs_dir), 'contact.log'),
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

@app.route('/')
def index():
    return render_template('resume.html', title='Резюме')

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

#@app.route('/contacts', methods=['GET', 'POST'])
#def contacts():
#    submitted = False
#    name = None
#    if request.method == 'POST':
#        name = request.form.get('name')
#        submitted = True
#    return render_template('contacts.html', title='Контакти', submitted=submitted, name=name)

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data

        logging.info("Contact form submitted: name=%s email=%s phone=%s subject=%s message=%s",
                     name, email, phone, subject, message)

        flash(f"Повідомлення від {name} ({email}) успішно прийнято.", "success")

        return redirect(url_for('contacts') + '?submitted=1')

    submitted = request.args.get('submitted') == '1'
    return render_template('contacts.html', title='Контакти', form=form, submitted=submitted)