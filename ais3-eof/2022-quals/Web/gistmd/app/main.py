from rq import Queue
from redis import Redis
from flask import Flask, render_template, request, g, redirect, session

import sqlite3
import secrets
import os
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe()
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

app.queue = Queue(connection=Redis('xss-bot'))


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/db.sqlite3')
        db.row_factory = sqlite3.Row
    return db


@app.before_first_request
def server_start():
    cursor = db().cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "users" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "username"  TEXT,
        "password"  TEXT
    );

    CREATE TABLE IF NOT EXISTS "notes" (
        "user_id"       INTEGER,
        "note_id"       TEXT,
        "title"         TEXT,
        "content"       TEXT
    );
    ''')
    cursor.execute("SELECT * FROM users WHERE username='administrator'")
    if cursor.fetchone() == None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ('administrator', os.getenv('ADMIN_PASSWORD', 'password')))
        note_id = secrets.token_urlsafe(16)
        cursor.execute("INSERT INTO notes (user_id, note_id, title, content) VALUES (?,?,?,?)",
                       (1, note_id, "FLAG", os.getenv("FLAG", "TEST_FL4G{meow}")))
    db().commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect("/login")
    user_id = session['user_id']
    cursor = db().cursor()
    query = "SELECT * FROM notes WHERE user_id=?"
    res = cursor.execute(query, (user_id,)).fetchall()
    return render_template('index.html', notes=res)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if len(username) < 8 or len(password) < 8:
            return render_template("login.html", error="Username or password too short (at least 8 chars)")

        cursor = db().cursor()
        query = "SELECT id, username, password FROM users WHERE username=?"
        res = cursor.execute(query, (username,)).fetchone()
        if res == None:
            # auto register
            query = "INSERT INTO users (username, password) VALUES (?,?)"
            user_id = cursor.execute(query, (username, password,)).lastrowid
            session['user_id'] = user_id
            db().commit()
            return redirect("/")
        elif res['password'] == password:
            session['user_id'] = res['id']
            return redirect("/")
        else:
            return render_template("login.html", error="Password incorrect.")

    return render_template("login.html")


@app.route('/note/<note_id>')
def note(note_id):
    cursor = db().cursor()

    query = "SELECT * from notes where note_id=?"
    cursor.execute(query, (note_id, ))
    res = cursor.fetchone()
    if res == None:
        return 'No such note.', 404

    return render_template('note.html', note=res)


@app.route('/note/<note_id>/raw')
def raw_note(note_id):
    cursor = db().cursor()

    query = "SELECT * from notes where note_id=?"
    cursor.execute(query, (note_id, ))
    res = cursor.fetchone()
    if res == None:
        return 'No such note.', 404

    return res['content'], 200, {'Content-Type': 'text/plain'}


@app.route('/report/<note_id>', methods=['POST'])
def report(note_id):
    # report to xss bot
    if 'user_id' not in session:
        return redirect("/login")

    cursor = db().cursor()
    query = "SELECT * from notes where note_id=?"
    cursor.execute(query, (note_id, ))
    if cursor.fetchone() == None:
        return 'No such note.', 404

    result = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
        'secret': app.config['RECAPTCHA_PRIVATE_KEY'],
        'response': request.form.get('g-recaptcha-response'),
        'remoteip': request.remote_addr,
    }).json()

    if not result['success']:
        return 'Invalid reCaptcha.', 403

    app.queue.enqueue("xssbot.browse", note_id)
    return 'OK', 200


@ app.route('/new', methods=['GET'])
def new_note():
    if 'user_id' not in session:
        return redirect("/login")
    return render_template('new.html')


@ app.route('/new', methods=['POST'])
def create_note():
    if 'user_id' not in session:
        return redirect("/login")

    if session['user_id'] == 1:
        return "Don't do that hackers, go caputre your flag!", 403

    note_id = secrets.token_urlsafe(16)
    cursor = db().cursor()
    query = "INSERT INTO notes (user_id, note_id, title, content) VALUES (?,?,?,?)"
    cursor.execute(query, (session['user_id'], note_id,
                   request.form['title'], request.form['content']))
    db().commit()
    return redirect(f'/note/{note_id}')


if __name__ == '__main__':
    app.run(debug=True)
