import sys, os

TARGET = 'com.xcv58.log:'
MAX_LENGTH = 36000
MAX_LENGTH = 10000

def usage():
    print 'Please follow the log file as first argument!'
    return

def oneFile(file_name, gap):
    f = open(file_name, 'r')
    logs = []
    previous = -1
    line_num = 0
    for line in f:
        line_num += 1
        logs.append(str(line_num) + " " + line[:-1])
        if TARGET in line:
            current = int(line.split(' ')[-1])
            if previous == -1:
                previous = current
            else:
                if current - previous > 1000 + gap:
                    print '--------------------------------'
                    print 'From line %s to %s, gap is %s milliseconds' % (line_num - len(logs), line_num, current - previous - 1000)
                    for log in logs:
                        print log
                previous = current
                pass
            logs = []
            pass
        pass
    f.close()

def main(argv):
    if len(argv) < 1 or not os.path.isfile(argv[0]):
        usage()
        return
    if len(argv) < 2:
        gap = 100
    else:
        gap = int(argv[1])
    oneFile(argv[0], gap)
    return

main(sys.argv[1:])
