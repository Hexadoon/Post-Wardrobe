'''
File for comunicating with the database
'''

# import uuid
import sqlite3
import datetime

# DB_FILE = '/var/www/Dress/Dress/data/hbr.db'
DB_FILE = 'data/dress.db'


def create_db():
    '''
    Creates the tables in the DB file
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, \
              password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS messages(msg_from TEXT, msg_to TEXT, \
               message TEXT, timestamp BLOB)')

    db.commit()
    db.close()

    return True


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


def user_exists(username):
    '''
    True if username is in DB
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    check = c.fetchone()

    return check is not None


def signup_attempt(username, password):
    '''
    Attempt to sign up
    Return True if username does not exist and has been added
    '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if user_exists(username):
        return False

    c.execute('INSERT INTO users VALUES(?, ?)', (username, password))

    db.commit()
    db.close()

    return True


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

    c.execute('SELECT msg_to FROM messages WHERE msg_from = ?', (sender,))
    set1 = c.fetchall()

    c.execute('SELECT msg_from FROM messages WHERE msg_to = ?', (sender,))
    set2 = c.fetchall()

    combolist = set1 + set2
    finalset = list(set(map(lambda x: x[0], combolist)))

    print(finalset)
    return set


def test():
    add_message('Joan', 'Kevin', 'Hello')
    add_message('Joan', 'Kevin', 'Hello???')
    add_message('Joan', 'Kevin', 'Hello??????')
    add_message('Kevin', 'Joan', 'Yuh whassup')
    add_message('Joan', 'Brandon', 'Hey')

    get_recipient_list('Joan')
    get_recipient_list('Kevin')
    get_recipient_list('Brandon')
    get_messages('Joan', 'Kevin')
    get_messages('Kevin', 'Joan')
    get_messages('Kevin', 'Joa')


if __name__ == '__main__':
    create_db()
    test()
