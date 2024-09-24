from flask import Flask, render_template
import re
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/indie")
def indie():
    render_template("indie.html")
    header = "this is an indie playlist generator"
    return render_template("indie.html")

@app.route("/house")
def house():
    header = "this is a house playlist generator"
    return header

if __name__ == "__main__":
    app.run()