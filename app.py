from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', name="test")


# FLASK_APP=app.py FLASK_ENV=development flask run