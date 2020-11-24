from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', name="test")


@app.route('/graph', methods=['POST'])
def graph():
    slope = request.form['slope']
    y_int = request.form['y-intercept']
    return render_template('index.html', slope=slope, y_int=y_int)

# FLASK_APP=app.py FLASK_ENV=development flask run
