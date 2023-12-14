from flask import Flask, render_template, url_for, request, redirect, flash

from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config["SECRET_KEY"]="2gfdgsd"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]=False
toolbar = DebugToolbarExtension(app)

app.logger.setLevel(logging.DEBUG)
app.logger.critical("fatal error")
app.logger.debug("debug")

app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))




@app.route("/")
def index():
    return "Hello, Flaskbook!"

@app.route("/hello/<name>",
           methods=["GET", "POST"],
           endpoint="hello-endpoint")
def show_name(name):
    return render_template("index.html", name=name)

@app.route("/hello2/<name>",
           methods=["GET", "POST"])
def show_name(name):
    return render_template("index1.html", name=name)

@app.route("/light_check/<command>",
           methods=["GET","POST"])
def light_check(command):
    return render_template("light_check.html", command=command)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete",
           methods=["GET", "POST"])
def contact_complete():
    if request.method=="POST":
        username =request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

    #    디버깅방법
    #    print(username)


        is_valid = True

        if not username:
            flash("사용자명 입력해라")
            is_valid=False

        if not email:
            flash("메일 써라")
            is_valid = False

        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash("메일 똑바로 써라")
            flash(str(e))
            is_valid = False
            
        if not description:
            flash("글 써라")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        send_email(email, "Reque Thx", "contact_mail", username=username, description=description)

        return redirect(url_for("contact_complete"))
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body=render_template(template+".txt", **kwargs)
    msg.html=render_template(template+".html", **kwargs)
    mail.send(msg)


""" with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="AK", page="1")) """

