import matplotlib
from flask import Flask, render_template, request
from matplotlib import pyplot as plt

matplotlib.use('Agg')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

xVals = []
yVals = []
minY = 0
maxY = 0
smartScale = "yes"

# home page for web application
@app.route('/')
def home():
    return render_template('index.html')

# establishs the domain [-10, 10] for which 
# coresponding Y values are computed
def xvalueAdd():
    start = -10
    for x in range(700):
        xVals.append(start)
        start += .03

# called when the user enter's a graphable filter
# collects data from the user based on which fucntion they want to graph
@app.route('/graph', methods=['POST'])
def graph():
    plt.clf()
    clearAll()
    xvalueAdd()
    function = request.form['function']
    global smartScale
    smartScale = request.form['smartscale']
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
    elif function == "cubic":
        a = request.form['ca']
        b = request.form['cb']
        c = request.form['cc']
        d = request.form['cd']
        cubic(a, b, c, d)
        return render_template('index.html', a=a, b=b, c=c, d=d, error=function)
    return render_template('index.html', error=function)

# computes Y values from the domain [-10, 10] for
# all linear functions
def linear(slope, y_int):
    global maxY
    global minY
    maxY = 0
    minY = 0
    for value in xVals:
        yValue = value * int(slope)
        if yValue > maxY:
            maxY = yValue
        if yValue < minY:
            minY = yValue
        yVals.append(yValue + int(y_int))
    graphing()

# computes Y values from the domain [-10, 10] for
# all quadratic functions
def quadratic(a, b, c):
    global maxY
    global minY
    maxY = 0
    minY = 0
    for value in xVals:
        yValue = (value * value) * int(a)
        yValue += value * int(b)
        yValue += int(c)
        if yValue > maxY:
            maxY = yValue
        if yValue < minY:
            minY = yValue
        yVals.append(yValue)
    graphing()

# computes Y values from the domain [-10, 10] for
# all cubic functions
def cubic(a, b, c, d):
    global maxY
    global minY
    maxY = 0
    minY = 0
    print(a)
    print(type(a))
    for value in xVals:
        yValue = (value ** 3) * int(a)
        yValue += value * value * int(b)
        yValue += value * int(c)
        yValue += int(d)
        if yValue > maxY:
            maxY = yValue
        if yValue < minY:
            minY = yValue
        yVals.append(yValue)
    graphing()

# clears all points from previous entry
def clearAll():
    xVals.clear()
    yVals.clear()

# plots all of the points that are computed and stored
# allows users to pick a dynamically scaled range to graph Y values
# saves an image file for the coresponding graph
def graphing():
    plt.scatter(xVals, yVals)
    plt.grid(True)
    plt.autoscale(False)
    plt.xlim((-10, 10))
    if smartScale == "yes":
        plt.ylim(minY * 1.1, maxY * 1.1)
    else:
        plt.ylim(-30, 30)
    plt.savefig('static/graph.png')

# manually disables caching of all image files and data on between each use
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

