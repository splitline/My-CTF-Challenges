#!/usr/bin/env python3
from os import getenv, urandom
from flask import Flask, g, request, session, send_file, render_template
import sqlite3
import re
import secrets

app = Flask(__name__)
app.secret_key = urandom(32)


def is_bad(payload):
    """ Weak WAF :)"""
    if re.search("replace|printf|char|[\\x00-\\x20]", payload, re.I | re.A):
        return True
    return False


class Flag():
    def __str__(self):
        if session.get('is_admin', False):
            return getenv("FLAG", 'FLAG{F4K3_FL4G}')
        else:
            return "Oops, You're not admin (・へ・)"


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('sqlite.db')
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    session['is_admin'] = False
    return render_template("index.html", token=f"GUEST-{secrets.token_hex(16).upper()}")


@app.route("/hint")
def hint():
    filename = request.args.get("file")
    if filename.endswith(".py"):
        return "Denied: *.py"
    return send_file(filename)


@app.route('/login', methods=["POST"])
def login():
    flag = Flag()
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    token = request.form.get('token', '')

    if is_bad(username) or is_bad(password):
        return "BAD!"

    if username != "admin" and re.search("ADMIN", token, re.I | re.A):
        return "Hey {username}, admin's token is not for you (・へ・)".format(username=username)

    cursor = db().cursor()
    query = f"SELECT username, password FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    res = cursor.fetchone()
    if res != None and res['username'] == username and res['password'] == password:
        if token.upper() == "ADMIN-E864E8E8F230374AA7B3B0CE441E209A":
            return ("Hello, " + username + " ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡  Here is your flag: {flag}").format(flag=flag)
        else:
            return ("Hello, " + username + " ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡  No flag for you (´;ω;`)")
    else:
        return f"No (´;ω;`)"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
