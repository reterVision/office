from flask import Flask, render_template, request, session
from flask.ext import pigeon
import pymongo
from forms import SignUpForm, SignInForm
from lib import redirect_back
from lib.decorator import login_required, crossdomain
from models import user
from models.exceptions import DoesNotExist, UserPasswordNotMatch
from settings import DEBUG, CONNECTION_STRING, DATABASE, SUPPORT_LANGUAGES


COOKIE = "DEV_COOKIE"
app = Flask("APP")
app.secret_key = "Development Key"
pigeon = pigeon.Pigeon(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signin", methods=["GET", "POST"])
@crossdomain("/signin")
def signin():
    form = SignInForm(request.form)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            remember = form.remember.data
            connection = pymongo.Connection(CONNECTION_STRING,
                                            safe=True)
            response = None
            try:
                username = user.validate_login(connection[DATABASE],
                                               username, password)
            except DoesNotExist:
                pigeon.error("You haven't registered yet!")
                response = app.make_response(redirect_back("signup"))
            except UserPasswordNotMatch:
                pigeon.error("Wrong username/password combination!")
                response = app.make_response(render_template("signin.html",
                                                             form=form))
            if not response:
                session_id = user.start_session(connection[DATABASE],
                                                username)
                if session_id == -1:
                    pigeon.error("Internal error!")
                else:
                    cookie = user.make_secure_val(session_id)

                    # Set cookies to client.
                    session_id = user.start_session(connection[DATABASE],
                                                    username)
                    cookie = user.make_secure_val(session_id)
                    redirect_to_home = redirect_back("index")
                    response = app.make_response(redirect_to_home)
                    response.set_cookie(COOKIE, value=cookie)

                    # Mark this user has logged in.
                    session["logged_in"] = True
                    session["username"] = username
                    return response
            else:
                return response

    return render_template("signin.html", form=form, status="signin")


@app.route("/signup", methods=["GET", "POST"])
@crossdomain("/signup")
def signup():
    form = SignUpForm(request.form)
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            connection = pymongo.Connection(CONNECTION_STRING,
                                            safe=True)

            message = {"error": None}
            if not user.newuser(connection[DATABASE],
                                username, email, password, message):
                pigeon.error(message["error"])
            else:
                pigeon.success(u"Welcome to Office! Your local gist!")

                # Set cookies to client.
                session_id = user.start_session(connection[DATABASE], username)
                cookie = user.make_secure_val(session_id)
                redirect_to_home = redirect_back("index")
                response = app.make_response(redirect_to_home)
                response.set_cookie(COOKIE, value=cookie)

                # Mark this user has logged in.
                session["logged_in"] = True
                session["username"] = username
                return response

    return render_template("signup.html", form=form, status="signup")


@app.route("/signout")
def signout():
    cookie = request.cookies.get(COOKIE, None)
    session["logged_in"] = False
    session["username"] = None

    if cookie is None:
        return redirect_back("signin")
    else:
        session_id = user.check_secure_val(cookie)

        if session_id is None:
            return redirect_back("signin")
        else:
            connection = pymongo.Connection(CONNECTION_STRING,
                                            safe=True)
            user.end_session(connection[DATABASE], session_id)
            redirect_to_signin = redirect_back("signin")
            response = app.make_response(redirect_to_signin)
            response.set_cookie(COOKIE, value="")
            return response


@app.route("/gist/new", methods=["GET", "POST"])
@crossdomain("/gist/new")
@login_required
def gist_new():
    if request.method == "POST":
        pass

    return render_template("new.html",
                           status="new", lang_list=SUPPORT_LANGUAGES)


@app.route("/gist/<username>")
@login_required
def gist_list(username):
    return render_template("list.html", status="list")


if __name__ == "__main__":
    app.run(port=5000, debug=DEBUG)
