from flask import Flask, render_template, request, session
from flask.ext import pigeon
import pymongo
from settings import DEBUG


app = Flask("APP")
pigeon = pigeon.Pigeon(app)


@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=5000, debug=DEBUG)
