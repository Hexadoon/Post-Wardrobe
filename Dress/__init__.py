'''
Main file for Dress Rental Flask app
'''

import datetime as dt
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
    username, password = request.form['username'], request.form['password']
    if db.login_attempt(username, password):
        session['username'] = username
        return redirect(url_for("browse"))
    else:
        flash('Email or password incorrect!', 'pink')
        return redirect(request.referrer)


@app.route('/signup', methods=["POST"])
def signup():
    '''
    Attempt to sign up
    Flash if failure
    Redirect to index
    '''
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    if db.signup_attempt(username, email, password):
        session['username'] = username
        return redirect(url_for("browse"))
    else:
        flash('Username or email already exists!')
        return redirect(url_for('signup_page'))


@app.route('/choose')
def choose():
    return render_template('choose.html')


@app.route('/browse', methods=["GET", 'POST'])
def browse():
    return render_template('browse.html')


@app.route('/signup_page')
def signup_page():
    return render_template('signup_page.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('browse'))


@app.route('/getitem', methods=["POST"])
def get_item():

    tags = {}

    item_no = int(request.form['item_no'])
    tags['size'] = request.form['size']
    tags['material'] = request.form['material']
    tags['color'] = request.form['color']
    tags['price'] = request.form['price']
    tags['occassion'] = request.form['occassion']
    tags['weather'] = request.form['weather']
    tags['condition'] = request.form['condition']

    new_tags = dict(tags)

    for key, value in tags.items():
        if value == 'Any':
            del new_tags[key]

    tags = new_tags

    item = db.get_item(item_no, tags=tags)

    if item is None:
        return 'Unavailable'
    elif item == 'Done':
        return 'No more'

    '''item_id TEXT PRIMARY KEY, \
               img_src TEXT, name TEXT, price REAL, available INT, size TEXT, \
               material TEXT, color TEXT, occassion TEXT, weather TEXT, \
               condition TEXT'''

    d = {}
    d['item_id'] = 'item_' + str(item_no)
    d['name'] = item[2]
    d['suggested_price'] = item[3]
    d['img_src'] = item[1]
    d['price'] = item[3]
    print(render_template('browse_item.html', **d))
    return render_template('browse_item.html', **d)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/messages')
def messages():
    if 'username' not in session:
        flash('You must be logged in to do that', 'pink')
        return redirect(url_for('browse'))
    username = session['username']
    peeps = db.get_recipient_list(username)

    d = {}
    for peep in peeps:
        name = peep[0]
        timestamp = dt.datetime.fromisoformat(peep[1])
        if name in d:
            if timestamp > d[name]:
                d[name] = timestamp
        else:
            d[name] = timestamp

    people = list(map(lambda x: [x[0], x[1].strftime('%d %b %Y, %I:%M %p')],
                  sorted(list(d.items()), key=lambda x: x[1])))
    return render_template('messages.html', people=people)


@app.route('/message/<recipient>')
def message(recipient):
    return render_template('message.html')


@app.route('/get_messages', methods=["POST"])
def get_messages():
    sender = session['username']
    recipient = request.form['recipient']

    set1, set2 = db.get_messages(sender, recipient)
    messages = list(map(list, set1 + set2))
    # print(messages)
    messages = list(map(lambda x: x[:3] + [dt.datetime.fromisoformat(x[3])],
                        messages))
    messages = sorted(messages, key=lambda x: x[3])
    messages = list(map(lambda x: x[:3] + [x[3].strftime('%d %b %Y, %I:%M %p')],
                        messages))

    '''
    CREATE TABLE IF NOT EXISTS messages(msg_from TEXT, msg_to TEXT,\
               message TEXT, timestamp BLOB
    '''

    return render_template('message_template.html', messages=messages)


@app.route('/send_message', methods=["POST"])
def send_message():
    sender = session['username']
    recipient = request.form['recipient']
    message = request.form['msg']

    db.add_message(sender, recipient, message)

    return "Done"


@app.route('/item/<item_id>')
def item(item_id):
    '''
    (item_id, img_src, name, price, available, size, material, color,
     occassion, weather, condition, seller)
    '''
    item = db.get_item_info(item_id)

    d = {}
    d['imgs'] = [item[1]]
    d['name'] = item[2]
    d['seller_name'] = item[-2]
    d['description'] = item[-1]
    d['price'] = item[3]

    return render_template('item.html', **d)


@app.route('/redir_main')
def redir_main():
    if 'username' in session:
        return redirect(url_for('browse'))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.debug = True
    app.run()
