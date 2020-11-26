import matplotlib
from flask import Flask, render_template, request
from matplotlib import pyplot as plt

matplotlib.use('Agg')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

xVals = []
yVals = []


@app.route('/')
def hello_world():
    return render_template('index.html', name="test")


def xvalueAdd():
    start = -10
    for x in range(640):
        xVals.append(start)
        start += .03


@app.route('/graph', methods=['POST'])
def graph():
    plt.clf()
    slope = request.form['slope']
    y_int = request.form['y-intercept']
    xVals.clear()
    yVals.clear()
    xvalueAdd()
    for value in xVals:
        yValue = value * int(slope)
        yVals.append(yValue + int(y_int))
    plt.scatter(xVals, yVals)
    plt.grid(True)
    plt.autoscale(False)
    plt.xlim((-10, 10))
    plt.ylim((-30, 30))

    plt.savefig('static/graph.png')
    return render_template('index.html', slope=slope, y_int=y_int)


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# FLASK_APP=app.py FLASK_ENV=development flask run
