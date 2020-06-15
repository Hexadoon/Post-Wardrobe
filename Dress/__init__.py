'''
Main file for Dress Rental Flask app
'''

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/browse')
def browse():
    return render_template('browse.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
