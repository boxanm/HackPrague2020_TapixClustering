from flask import render_template
from form import LoginForm
from main import app

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)