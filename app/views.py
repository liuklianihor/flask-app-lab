from flask import Flask, render_template, request, url_for # type: ignore
from . import app

@app.route('/')
def index():
    return render_template('resume.html', title='Резюме')

@app.route('/resume')
def resume():
    return render_template('resume.html', title='Резюме')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    submitted = False
    name = None
    if request.method == 'POST':
        name = request.form.get('name')
        submitted = True
    return render_template('contacts.html', title='Контакти', submitted=submitted, name=name)