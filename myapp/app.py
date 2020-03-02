from flask import Flask
from flask import render_template, request, url_for, redirect, escape, session
# from custom_session import CustomSessionInterface
# import flask_login


app = Flask(__name__)
app.config['SECRET_KEY'] = "keepitsecret"
# app.session_interface = CustomSessionInterface()


@app.errorhandler(404)
def page_not_found(error):
    return render_template("main/404.html"), 404


@app.route('/')
def index():
    if 'username' in session:
        return render_template("main/index.html", user=session['username'])
    return render_template("main/index.html")


@app.route("/add_game", methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        name = request.form['game_name']
        rdate = request.form['game_rdate']
        rate = request.form['game_rate']
        return escape("Added: " + name + '\n' + rdate + '\n' + rate)
    return render_template("main/add_game.html")

# def valid_login(username, password):
#     return True


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username') is not None:
        return redirect(url_for("index"))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # remember = request.form.get('remember')
        valid = True
        # if valid_login(username, password):

        if username != 'admin':
            valid = False
        elif password != '123':
            valid = False

        if valid:
            session['username'] = username
            # if remember == 'on':
            #     session.permanent = True
            #     print('save')
            # else:
            #     session.permanent = False
            return redirect(url_for("success", what='login'))
        else:
            return render_template("auth/login.html", is_invalid=not valid)

    return render_template("auth/login.html")


@app.route("/logout")
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/success")
def success():
    return render_template("auth/success.html", what=request.args.get('what'))


@app.route('/user/<username>')
def user_profile(username):
    if session.get('username') is None:
        return redirect(url_for('index'))
    user = session['username']
    if username != user:
        return escape(username) + " user not found"
    # name = username
    return render_template("main/user_profile.html", user=user, name=user)


@app.route("/hello")
def hello():
    user = 'World'
    if 'username' in session:
        user = session['username']
    return render_template("main/hello.html", user=user)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    # https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiv-ajax
    # https://github.com/anfederico/Flaskex/blob/master/app.py
    # https://palletsprojects.com/p/flask/
    # https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.session
