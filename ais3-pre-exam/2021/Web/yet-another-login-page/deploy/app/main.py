from flask import Flask, request, make_response, redirect, session, render_template, send_file
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(32)

FLAG = os.environ.get('FLAG', 'AIS3{TEST_FLAG}')
users_db = {
    'guest': 'guest',
    'admin': os.environ.get('PASSWORD', 'S3CR3T_P455W0RD')
}


@app.route("/")
def index():
    def valid_user(user):
        return users_db.get(user['username']) == user['password']

    if 'user_data' not in session:
        return render_template("login.html", message="Login Please :D")

    user = json.loads(session['user_data'])
    if valid_user(user):
        if user['showflag'] == True and user['username'] != 'guest':
            return FLAG
        else:
            return render_template("welcome.html", username=user['username'])

    return render_template("login.html", message="Verify Failed :(")


@app.route("/login", methods=['POST'])
def login():
    data = '{"showflag": false, "username": "%s", "password": "%s"}' % (
        request.form["username"], request.form['password']
    )
    session['user_data'] = data
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/sauce")
def sauce():
    return send_file(__file__, mimetype="text/plain")


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
