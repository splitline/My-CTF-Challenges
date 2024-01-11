from flask import Flask, request, redirect, jsonify, send_file
import re

# db.py: not provided
from db import db

app = Flask(__name__)


@app.before_request
def fix_path():
    # trim all the whitespace from path
    trimmed = re.sub('\s+', '', request.path)
    if trimmed != request.path:
        return redirect(trimmed)


@app.route('/')
def index():
    return send_file('index.html')


@app.route('/api/all')
def emojis():
    cursor = db().cursor()
    cursor.execute("SELECT Name FROM Emoji")
    return jsonify(cursor.fetchall())


@app.route('/api/emoji/<unicode>')
def api(unicode):
    cursor = db().cursor()
    cursor.execute("SELECT * FROM Emoji WHERE Unicode = %s" % unicode)
    row = cursor.fetchone()
    if row:
        return jsonify({'data': row})
    else:
        return jsonify({'error': 'Cat emoji not found'})


@app.route('/source')
def source():
    return send_file(__file__, mimetype='text/plain')
