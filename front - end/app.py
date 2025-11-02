from flask import Flask, render_template, request, redirect, url_for, flash
#from flask_mail import Mail, Message

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/aboutus")
def aboutus():
    return render_template("aboutus1.html")

@app.route("/contct")
def contact():
    return render_template("contact1.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/forgotpass")
def forgotpassword():
    return render_template("forgot-password.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery1.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/roomlist")
def roomlist():
    return render_template("roomlist-2.html")

@app.route("/roomdetail")
def roomdetail():
    return render_template("detail-full.html")

@app.route("/availability")
def availability():
    return render_template("availability.html")

@app.route("/roomselect")
def roomselect():
    return render_template("room-select.html")

@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/checkout")
def checkout():
    return render_template("checkout.html")

@app.route("/confirmation")
def confirmation():
    return render_template("confirmation.html")

if __name__ == "main":
    app.run("localhost", port=8000, debug=True)