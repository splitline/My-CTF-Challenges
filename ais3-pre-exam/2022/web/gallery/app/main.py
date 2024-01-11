from flask import Flask, render_template, request, redirect, url_for, g, session, send_file
import sqlite3
import secrets
import os
import uuid
import mimetypes
import pathlib

from rq import Queue
from redis import Redis

app = Flask(__name__)
app.queue = Queue(connection=Redis('xss-bot'))
app.config.update({
    'SECRET_KEY': secrets.token_bytes(16),
    'UPLOAD_FOLDER': '/data/uploads',
    'MAX_CONTENT_LENGTH': 32 * 1024 * 1024,  # 32MB
})

IMAGE_EXTENSIONS = [ext for ext, type in mimetypes.types_map.items()
                    if type.startswith('image/')]

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
FLAG_UUID = os.getenv('FLAG_UUID', str(uuid.uuid4()))


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/db.sqlite3')
        db.row_factory = sqlite3.Row
    return db


@app.before_first_request
def create_tables():
    cursor = db().cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        );
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            title TEXT,
            filename TEXT,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if cursor.fetchone() == None:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ('admin', ADMIN_PASSWORD))
        admin_id = cursor.lastrowid
        cursor.execute("INSERT INTO images (user_id, uuid, filename, title) VALUES (?, ?, ?, ?)",
                       (admin_id, FLAG_UUID, FLAG_UUID+".png", "FLAG"))

    db().commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.after_request
def add_csp(response):
    response.headers['Content-Security-Policy'] = ';'.join([
        "default-src 'self'",
        "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com"
    ])
    return response


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    cursor = db().cursor()
    cursor.execute("SELECT * FROM images WHERE user_id=?",
                   (session['user_id'],))
    images = cursor.fetchall()
    return render_template('index.html', images=images)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if len(username) < 5 or len(password) < 5:
            return render_template('login.html', error="Username and password must be at least 5 characters long.")
        cursor = db().cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                           (username, password))
            user_id = cursor.lastrowid
            session['user_id'] = user_id
            return redirect(url_for('index'))
        elif user['password'] == password:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")


@app.route('/image/<uuid>')
def view(uuid):
    cursor = db().cursor()
    cursor.execute("SELECT * FROM images WHERE uuid=?", (uuid,))
    image = cursor.fetchone()
    if image:
        if image['user_id'] != session['user_id']:
            return "You don't have permission to view this image.", 403
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], image['filename']))
    else:
        return "Image not found.", 404


@app.route('/image/<uuid>/download')
def download(uuid):
    cursor = db().cursor()
    cursor.execute("SELECT * FROM images WHERE uuid=?", (uuid,))
    image = cursor.fetchone()
    if image:
        if image['user_id'] != session['user_id']:
            return "You don't have permission to download this image.", 403
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], image['filename']), as_attachment=True, mimetype='application/octet-stream')
    else:
        return "Image not found.", 404


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        title = request.form['title'] or '(No title)'
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error="No file selected")

        extension = pathlib.Path(file.filename).suffix
        if extension not in IMAGE_EXTENSIONS:
            return render_template('upload.html', error="File must be an image")

        image_uuid = str(uuid.uuid4())
        filename = image_uuid + extension
        cursor = db().cursor()
        cursor.execute("INSERT INTO images (user_id, uuid, title, filename) VALUES (?, ?, ?, ?)",
                       (session['user_id'], image_uuid, title, filename))
        db().commit()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))


@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return f'''
        <h1>Report to admin</h1>
        <p>注意：admin 會用 <code>http://web/</code> （而非 {request.url_root} 作為 base URL 來訪問你提交的網站。</p>
        <form action="/report" method="POST">
            <input type="text" name="url" placeholder="URL ({request.url_root}...)">
            <input type="submit" value="Submit">
        </form>
        '''
    else:
        url = request.form['url']
        if url.startswith(request.url_root):
            url_path = url[len(request.url_root):]
            app.queue.enqueue('xssbot.browse', url_path)
            return 'Reported.'
        else:
            return f"[ERROR] Admin 只看 {request.url_root} 網址"
