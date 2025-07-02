from flask import Flask, render_template, redirect


app = Flask(__name__)


counter = 0

@app.route("/")
def index():
    return render_template("index.html", counter=counter)


@app.route("/click")
def count():
    global counter
    counter += 1
    return redirect("/")

