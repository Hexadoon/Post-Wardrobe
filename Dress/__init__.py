'''
Main file for Dress Rental Flask app
'''

from flask import (Flask, render_template, request, session, flash, redirect,
                   url_for)
from util import db

app = Flask(__name__)
app.secret_key = "beansbeansbeans"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    '''
    Attempt to login
    Flash if failure
    Redirects to index
    '''
    email, password = request.form['email'], request.form['password']
    if db.login_attempt(email, password):
        session['email'] = email
        return redirect(url_for("browse"))
    else:
        flash('Email or password incorrect!')
        return redirect(url_for("index"))


@app.route('/signup', methods=["POST"])
def signup():
    '''
    Attempt to sign up
    Flash if failure
    Redirect to index
    '''
    email, password = request.form['email'], request.form['password']
    if db.signup_attempt(email, password):
        session['email'] = email
        return redirect(url_for("browse"))
    else:
        flash('Email already exists!')
        return redirect(url_for('signup_page'))


@app.route('/choose')
def choose():
    return render_template('choose.html')


@app.route('/browse')
def browse():
    return render_template('browse.html')


@app.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    return redirect(url_for('browse'))


@app.route('/getitem', methods=["POST"])
def get_item():
    print(request.form)
    return """<div class="col-lg-4 col-md-6 mb-4">
                <div class="card zoom mx-5 mx-md-0">
                  <img class="card-img-top" src="https://images.www.fendi.com/images/h00/hc0/9046410821662/FZD832ABWQF1AKS_01_large-grey" alt="dress" style="height: 300px; object-fit: cover">
                  <div class="card-body">
                    <a class="h5 card-title stretched-link black-link" href="/item/itemid"><span class="float-left">Product name</span><span class="float-right">$25</span></a>
                  </div>
                </div>
              </div>"""


@app.route('/messages')
def messages():
    if 'username' not in session:
        return redirect(url_for('browse'))
    username = session['username']
    db.get_recipient_list(username)


@app.route('/message/<recipient>')
def message(recipient):
    return render_template('message.html')


@app.route('/get_messages')
def get_messages():
    sender = session['username']
    recipient = request.form['recipient']

    set1, set2 = db.get_messages(sender, recipient)
    messages = sorted(set1 + set2, key=lambda x: x[3])

    print(messages)
    return messages


@app.route('/send_message')
def send_message():
    sender = session['username']
    recipient = request.form['recipient']
    message = request.form['msg']

    db.send_message(sender, recipient, message)

    return "Done"


if __name__ == '__main__':
    app.debug = True
    app.run()
