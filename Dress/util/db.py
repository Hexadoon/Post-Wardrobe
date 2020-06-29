'''
File for comunicating with the database
'''

import uuid
import sqlite3
import datetime
import time

# DB_FILE = '/var/www/Dress/Dress/data/hbr.db'
DB_FILE = 'data/dress.db'


# TODO: Make the img_src a directory so you can store multiple images

def create_db():
    '''
    Creates the tables in the DB file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT PRIMARY KEY, \
               username TEXT, email TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages(msg_from TEXT, msg_to TEXT,\
               message TEXT, timestamp BLOB)')
    c.execute('CREATE TABLE IF NOT EXISTS items(item_id TEXT PRIMARY KEY, \
               img_src TEXT, name TEXT, price REAL, available INT, size TEXT, \
               material TEXT, color TEXT, occassion TEXT, weather TEXT, \
               condition TEXT, seller TEXT, description TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS misc(key TEXT PRIMARY KEY, \
               value TEXT)')

    c.execute('INSERT INTO misc VALUES(?, ?)', ('item_count', '0'))

    db.commit()
    db.close()

    return True


def get_item_count():
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value FROM misc WHERE key = ?', ('item_count',))
    item_count = c.fetchone()[0]

    return item_count


def add_item(name, src, price, tags):
    # Tags: (size, material, color, occassion, weather, condition)
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    item_count = get_item_count()
    item_id = 'item_' + item_count

    c.execute('INSERT INTO items VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (item_id, src, name, price, 1) + tags)

    c.execute('UPDATE misc SET value = ? WHERE KEY = ?',
              (str(int(item_count) + 1), 'item_count'))

    db.commit()
    db.close()

    return item_id


def get_item(item_no, tags=None):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT value FROM misc WHERE key=?', ('item_count',))
    item_count = int(c.fetchone()[0])

    if item_no > item_count:
        return 'Done'

    tag_list = []

    if tags is not None:
        for tag, value in tags.items():
            if tag == 'price':
                tag_list.append('price < {}'.format(str(value)))
            else:
                tag_list.append('{} = "{}"'.format(tag, value))

    tag_string = ' AND '.join(tag_list)
    if tag_string != '':
        tag_string = ' AND ' + tag_string

    s = 'SELECT * FROM items WHERE item_id = ? ' + \
        'AND available = 1 {}'.format(tag_string)
    print(s)
    c.execute(s, ('item_' + str(item_no),))

    item = c.fetchone()

    return item


def get_item_info(item_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT * FROM items WHERE item_id = ?', (item_id,))

    item = c.fetchone()

    return item


def login_attempt(username, password):
    '''
    Attempt to login
    Returns True if user/pass combo is correct
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    p = c.fetchone()

    if p is None:
        return False

    return password == p[0]


def user_exists(username, email):
    '''
    True if username/email is in DB
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    check1 = c.fetchone()

    c.execute('SELECT 1 FROM users WHERE email = ?', (email,))
    check2 = c.fetchone()

    return check1 is not None and check2 is not None


def signup_attempt(username, email, password):
    '''
    Attempt to sign up
    Return True if username/email does not exist and has been added
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if user_exists(username, email):
        return False

    user_id = str(uuid.uuid4())

    c.execute('INSERT INTO users VALUES(?, ?, ?, ?)', (user_id, username,
                                                       email, password))

    db.commit()
    db.close()

    return user_id


def add_message(sender, recipient, message):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    timestamp = datetime.datetime.now()
    c.execute('INSERT INTO messages VALUES(?, ?, ?, ?)',
              (sender, recipient, message, timestamp))

    db.commit()
    db.close()


def get_messages(sender, recipient):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT * FROM messages WHERE msg_from = ? AND msg_to = ?',
              (sender, recipient))
    set1 = c.fetchall()

    c.execute('SELECT * FROM messages WHERE msg_from = ? AND msg_to = ?',
              (recipient, sender))
    set2 = c.fetchall()

    print(sorted(set1 + set2, key=lambda x: x[3]))
    return set1, set2


def get_recipient_list(sender):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT msg_to, timestamp FROM messages WHERE msg_from = ?', (sender,))
    set1 = c.fetchall()

    c.execute('SELECT msg_from, timestamp FROM messages WHERE msg_to = ?', (sender,))
    set2 = c.fetchall()

    combolist = set1 + set2

    return combolist


def get_user_id(username=None, email=None):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    user_id = None

    if username is not None:
        c.execute('SELECT user_id FROM users WHERE user_id = ?', (username,))
        username = c.fetchone()

    elif email is not None:
        c.execute('SELECT user_id FROM users WHERE email = ?', (email,))
        username = c.fetchone()

    if user_id is not None:
        user_id = user_id[0]
    return user_id


def get_username(user_id=None, email=None):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    username = None

    if user_id is not None:
        c.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
        username = c.fetchone()

    elif email is not None:
        c.execute('SELECT username FROM users WHERE email = ?', (email,))
        username = c.fetchone()

    if username is not None:
        username = username[0]
    return username


def test():
    # user_id = signup_attempt('Joan', 'jchirinos3201@gmail.com', 'password')
    # print(get_username(user_id=user_id))
    # print(get_username(email='jchirinos3201@gmail.com'))
    # print(get_username(user_id='54'))

    # (name, src, price, tags):
    #     # Tags: (size, material, color, occassion, weather, condition)
    add_item('Cool dress', 'no source', 24.99,
             ('L', 'Cotton', 'Red', 'Prom', 'Warm', 'Like New'))
    add_item('Cool dress with quite a long name', 'no source', 24.99,
             ('L', 'Cotton', 'Red', 'Prom', 'Warm', 'Like New'))

    signup_attempt('Joan', 'jchirinos3201@gmail.com', 'password')

    add_message('Joan', 'Kevin', 'beans????')
    add_message('Joan', 'Kevin', 'benin????')
    add_message('Joan', 'Kevin', 'got it????')

    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    time.sleep(70)

    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')

    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')

    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')
    add_message('Joan', 'Kevin', 'got it????')

    add_message('Kevin', 'Joan', 'yes got it. jesus christ')

    add_message('Momther', 'Joan', 'do your work')


if __name__ == '__main__':
    create_db()
    test()
