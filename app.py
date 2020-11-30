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
    clearAll()
    xvalueAdd()
    function = request.form['function']
    if function == "linear":
        slope = request.form['slope']
        y_int = request.form['y-intercept']
        linear(slope, y_int)
        return render_template('index.html', slope=slope, y_int=y_int, error=function)
    elif function == "quadratic":
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        quadratic(a, b, c)
        return render_template('index.html', a=a, b=b, c=c, error=function)
    return render_template('index.html', error=function)


def quadratic(a, b, c):
    for value in xVals:
        yValue = (value * value) * int(a)
        yValue += value * int(b)
        yValue += int(c)
        yVals.append(yValue)
    graphing()


def clearAll():
    xVals.clear()
    yVals.clear()


def linear(slope, y_int):
    for value in xVals:
        yValue = value * int(slope)
        yVals.append(yValue + int(y_int))
    graphing()


def graphing():
    plt.scatter(xVals, yVals)
    plt.grid(True)
    plt.autoscale(False)
    plt.xlim((-10, 10))
    plt.ylim((yVals[0]-10, yVals[-1]+10))
    plt.savefig('static/graph.png')


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# FLASK_APP=app.py FLASK_ENV=development flask run
