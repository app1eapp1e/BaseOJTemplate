### DEPRACATED -- The file is in ./questions/help_tool
import os
import sys
def load_data(filename):
    try:
        return eval(open(filename, 'r').read())
    except SyntaxError:
        print("[-] Test IO Syntax Error")
        exit(-1)
def extract_test_ios(filename):
    try:
        data = load_data(filename)
        return data[3]
    
    except IndexError:
        print("[-] Extraction Error")
        exit(-1)

def extract_ios(filename):
    try:
        data = load_data(filename)
        return data[5]
    except IndexError:
        print("[-] Extraction Error")
        exit(-1)


def create_space(filename):
    path = os.path.dirname(filename)
    foldername = os.path.splitext(os.path.filename(filename))[0]
    try:
        os.mkdir(os.path.join(path, foldername))
        return os.path.join(path, foldername)
    except Exception:
        print("[-] Failed to create directory")
        exit(-1)

def add_ios(ios, path):
    i = 1
    for inp, out in ios:
        fd1 = open(os.path.join(path, '%s.in' % i), 'a')
        fd1.write(inp)
        fd1.flush()
        fd1.close()
        fd2 = open(os.path.join(path, '%s.out' % i), 'a')
        fd2.write(out)
        fd2.flush()
        fd2.close()

def add_test_ios(ios, path):
    i = 1
    for inp, out in ios:
        fd1 = open(os.path.join(path, 'test%s.in' % i), 'a')
        fd1.write(inp)
        fd1.flush()
        fd1.close()
        fd2 = open(os.path.join(path, 'test%s.out' % i), 'a')
        fd2.write(out)
        fd2.flush()
        fd2.close()

def create_file(data, path, name):
    try:
        fd = open(os.path.join(path, name), 'a')
        fd.write(data)
        fd.flush()
        fd.close()
    except Exception:
        print('[-] File Creation Exception')
        exit(-1)

def finish_compiling_process(filename):
    path = create_space(filename)
    test_ios = extract_test_ios(filename)
    ios = extract_ios(filename)
    add_ios(ios, path)
    add_test_ios(ios, path)
    data = load_data(filename)
    create_file(data[0], path, '.pdd')
    create_file(data[1], path, '.in_f')
    create_file(data[2], path, '.out_f')
    create_file(data[4], path, '.hnt')
    # No Solutions & statistics
    create_file('', path, '.ans')
    create_file('', path, '.stats')
    print('[+] Done')

if __name__ == '__main__':
    argv = sys.argv
    if len(argv)==1:
        print('Usage: %s [full_path/question.txt]' % argv[0])
    else:
        finish_compiling_process(argv[1])

