from flask import Flask, request, session, g, send_file, render_template, jsonify, redirect, send_from_directory
import uuid
import secrets
import time
import sqlite3
import json
import os

from redis import Redis
from rq import Queue

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
app.queue = Queue(connection=Redis('xssbot'))
app.config['SERVER_NAME'] = 'ctf-note.splitline.tw:9527'
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/db.sqlite3')
        db.row_factory = sqlite3.Row
    return db


@app.before_first_request
def server_start():
    cursor = db().cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "users" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "username"  TEXT NOT NULL,
        "password"  TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS "writeups" (
        "user_id"       TEXT,
        "uuid"          TEXT,
        "contest_name"  TEXT,
        "writeup_json"  TEXT
    )
    ''')
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE username='admin'")
    count = cursor.fetchone()['count']
    if count == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",
                       ('admin', os.getenv("PASSWORD")))
        cursor.execute("INSERT INTO writeups (user_id, uuid, contest_name, writeup_json) VALUES (?,?,?,?)",
                       ('admin', str(uuid.uuid4()), 'FLAG', json.dumps([{
                           "category": "Web",
                           "challenge": "I am the FLAG!",
                           "content": os.getenv("FLAG")
                       }])
                       ))
    db().commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.nonce = secrets.token_hex(16)


@app.after_request
def after_request(response):
    response.headers['Content-Security-Policy'] = ';'.join([
        "default-src 'none'",
        "base-uri 'none'",
        "img-src 'self'",
        "style-src 'self'",
        "connect-src 'self'",
        f"script-src 'strict-dynamic' 'nonce-{g.nonce}'"
    ])
    return response


@app.route('/plugins/<string:js>')
def plugins(js):
    return send_from_directory("plugins", js)


@app.route('/config.js')
def config():
    return send_file("config.js")


@app.route('/api/list')
def ctf_list():
    if session.get("username") == None:
        return "Login required."
    cursor = db().cursor()
    query = "SELECT uuid, contest_name from writeups where user_id=?"
    cursor.execute(query, (session['username'], ))
    res = cursor.fetchall()

    ctfs = list(map(lambda item: {
        "title": item['contest_name'],
        "uuid": item['uuid']
    }, res))
    return jsonify({"ctf": ctfs})


@app.route('/api/add', methods=["POST"])
def add_ctf():
    if session.get("username") == None:
        return "Login required."

    data = request.json
    writeups = map(lambda wp: {
        "category": str(wp.get('category')),
        "challenge": str(wp.get('challenge')),
        "content": str(wp.get('content'))
    }, data['writeups'])

    uuid4 = uuid.uuid4()
    cursor = db().cursor()
    query = "INSERT INTO writeups (user_id, uuid, contest_name, writeup_json) VALUES (?,?,?,?)"
    cursor.execute(query, (session['username'], str(uuid4),
                           data['contestName'],  json.dumps(list(writeups))))
    db().commit()
    return jsonify({"uuid": uuid4})


@app.route('/api/<string:ctf_id>')
def api(ctf_id):
    if session.get("username") == None:
        return "Login required."

    cursor = db().cursor()
    query = "SELECT * from writeups where uuid=?"
    cursor.execute(query, (ctf_id, ))
    res = cursor.fetchone()
    if res == None:
        return jsonify({"contestName": "(not found)", "writeups": []})
    else:
        return jsonify({
            "contestName": res["contest_name"],
            "writeups": json.loads(res["writeup_json"])
        })


@app.route("/api/enabled_plugins")
def enabled_plugins():
    time.sleep(0.05)
    return jsonify(['nyanCat'])


@app.route('/report', methods=['POST'])
def report():
    if session.get("username") == None:
        return "Login required."

    url = str(request.form.get('url'))
    if url.startswith(request.url_root):
        url_path = url[len(request.url_root):]
        app.queue.enqueue('xssbot.browse', url_path)
        return 'Reported.'
    else:
        return f"[ERROR] 我只收 {request.url_root} 上的 write-up ㄛ"


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == "" or password == "":
            return render_template("login.html", error="Empty username or password.")

        cursor = db().cursor()
        query = "SELECT username, password FROM users WHERE username=?"
        cursor.execute(query, (username,))
        res = cursor.fetchone()
        if res == None:
            query = "INSERT INTO users (username, password) VALUES (?,?)"
            cursor.execute(query, (username, password,))
            session['username'] = username
            db().commit()
            return redirect("/")
        elif res['password'] == password:
            session['username'] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Password incorrect.")
    else:
        return render_template("login.html")


@app.route('/')
def index():
    if session.get("username") == None:
        return redirect("/login")
    return render_template("index.html", nonce=g.nonce)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
