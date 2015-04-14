import sys, os
import plotly.plotly as py
from plotly.graph_objs import *

TARGET = 'com.xcv58.log:'
MAX_LENGTH = 36000

def usage():
    print 'Please follow the log directory as argument!'
    return

def oneFile(file):
    f = open(file, 'r')
    logs = []
    for line in f:
        if TARGET in line:
            logs.append(line)
        pass
    f.close()
    # get timetsamp for all logs
    logs = [i.split(' ')[-1] for i in logs]
    missList = [int(y) - int(x) - 1000 for (x, y) in zip(logs[:-1], logs[1:])]
    print len(missList)
    print len([i for i in missList if i == 0])
    print len([i for i in missList if i >= 0])
    print sum(missList)
    return missList[:MAX_LENGTH]

def walk(path):
    files = os.listdir(path)
    dataList = [oneFile(os.path.join(path, i)) for i in files]
    data = [Scatter(x=range(len(d)), y=d, name=file) for file, d in zip(files , dataList)]

    layout = Layout(
        title='SPEC on Board',
        xaxis=XAxis(
            title='timer fired count',
            showgrid=False,
            zeroline=False
        ),
        yaxis=YAxis(
            title='delay (millisecond)',
            showline=False
        )
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='basic-line')
    return

def main(argv):
    if len(argv) < 1 or not os.path.isdir(argv[0]):
        usage()
        return
    walk(argv[0])
    return

main(sys.argv[1:])
