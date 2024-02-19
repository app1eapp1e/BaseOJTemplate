"""Usage: {} pddfile input_format_file output_format_file \
test_ios_count [test*.in test*.out] hint_file ios_count \
[*.in *.out] output_file"""
import sys
import os

def err(msg):
    print('[-]', msg)
    exit(-1)

def get_file_text(file):
    try:
        fd = open(file, 'r')
        t = fd.read()
        fd.close()
        return t
    except Exception:
        err('Cannot read file %s' % file)

def join_ios(num, list_):
    l = []
    if num * 2 != len(list_):
        err('Bad number of IOs')
    for x in range(num):
        ind = get_file_text(list_.pop(0))
        oud = get_file_text(list_.pop(0))
        l.append([ind, oud])
    return l

def complete_context(args):
    des = get_file_text(args[0])
    input_format = get_file_text(args[1])
    output_format = get_file_text(args[2])
    try:
        ntest_io = int(args[3])
        print(ntest_io)
    except ValueError:
        err('Bad `ntest_io`')
    test_ios = args[4:4+ntest_io*2]
    print(test_ios)
    test_ios = join_ios(ntest_io, test_ios)
    print(test_ios)
    hint = get_file_text(args[4+ntest_io*2])
    args = args[5+ntest_io*2:]
    try:
        n_io = int(args[0])
        # print(n_io)
    except ValueError:
        err('Bad `n_io`')
    args.pop(0)
    ios = args[0:n_io*2]
    # print(ios)
    ios = join_ios(n_io, ios)
    return [des, input_format, output_format, test_ios, hint, ios]

def finish_process(argv):
    c = complete_context(argv[1:])
    text = repr(c)
    fd = open(argv[-1], 'w')
    fd.write(text)
    fd.flush()
    fd.close()
    print('[+] Done')

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 1:
        print(__doc__.format(argv[0]))
    else:
        finish_process(argv)
    
