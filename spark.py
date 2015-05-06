import sys, os

TARGET = 'com.xcv58.log:'
MAX_LENGTH = 36000
MAX_LENGTH = 10000

def usage():
    print 'Please follow the log file as first argument!'
    return

def oneFile(file_name, gap):
    tags_set = set()
    sparks = []
    f = open(file_name, 'r')
    logs = []
    previous = -1
    line_num = 0
    for line in f:
        line_num += 1
        if '--------- beginning of /dev/log' in line:
            continue
        tags_set.add(line.split()[5])
        logs.append(str(line_num) + " " + line[:-1])
        if TARGET in line:
            current = int(line.split(' ')[-1])
            if previous == -1:
                previous = current
            else:
                if current - previous > 1000 + gap:
                    # print '--------------------------------'
                    # print 'From line %s to %s, gap is %s milliseconds' % (line_num - len(logs), line_num, current - previous - 1000)
                    sparks.append([line_num, logs[:-1], current - previous - 1000])
                    # for log in logs:
                    #     print log
                previous = current
                pass
            logs = []
            pass
        pass
    f.close()
    processSparks(tags_set, sparks)
    pass

def processSparks(tags_set, sparks):
    tags_list = list(tags_set)
    for i in sparks:
        tags_dict = dict()
        for tag in tags_list:
            tags_dict.setdefault(tag, 0)
        line_num = i[0]
        lines = i[1]
        for line in lines:
            tag = line.split()[6]
            tags_dict[tag] = tags_dict[tag] + 1
            pass
        print 'From line %s to %s, gap is %s milliseconds' % (line_num - len(lines), line_num, i[2])
        for tag in tags_list:
            if tags_dict[tag] != 0:
                print tag, tags_dict[tag]
                pass
            pass
        print
        # print tags_dict
    pass


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
