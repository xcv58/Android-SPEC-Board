import sys, os
import plotly.plotly as py
from plotly.graph_objs import *
import collections
import numpy as np

TARGET = 'com.xcv58.log:'
MAX_LENGTH = 36000
MAX_LENGTH = 10000

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
    # print len(missList)
    # print len([i for i in missList if i == 0])
    # print len([i for i in missList if i >= 0])
    # print sum(missList)
    return missList

def walk(path):
    files = os.listdir(path)
    data_list = [oneFile(os.path.join(path, i)) for i in files]
    MAX_LENGTH = min([len(i) for i in data_list])
    data_list = [i[:MAX_LENGTH] for i in data_list]
    MAX_DELAY = max([max(i) for i in data_list])
    data_list = [collections.Counter(i) for i in data_list]
    cdf_list = []
    for c in data_list:
        x = [i for i in sorted(c)]
        y = [c[i] for i in x]
        y = np.divide(np.cumsum(y).astype(float), sum(y)).tolist()
        cdf_list += [[x, y]]
        pass
    data = [Scatter(x=d[0], y=d[1], name=file.replace('log-1-sec-1-process-', '').replace('.log', '')) for file, d in zip(files, cdf_list)]
    # cdf_list = [np.divide(np.cumsum(i).astype(float), sum(i)).tolist() for i in data_list]

    # print MAX_DELAY
    # print cdf_list

    # data = [Scatter(x=[1, 2, 3, 4], y=cdf) for file, d in zip(files, data_list)]

    # data = [Bar(x=range(MAX_LENGTH), y=d, name=file) for file, d in zip(files , data_list)]

    layout = Layout(
        title='SPEC on Board - CDF',
        xaxis=XAxis(
            title='delay (millisecond)',
            showgrid=False,
            zeroline=False
        ),
        yaxis=YAxis(
            title='CDF',
            showline=False
        ),
        barmode='stack'
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='cdf-spec')
    return

def main(argv):
    if len(argv) < 1 or not os.path.isdir(argv[0]):
        usage()
        return
    walk(argv[0])
    return

main(sys.argv[1:])
