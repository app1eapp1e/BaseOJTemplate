import os
from status import *
import shutil
import py_compile



def update_interpreter():
    global PYTHON
    current = os.path.dirname(__file__)
    os.chdir(current)
    PYTHON = open('./pypath.txt', 'r').read()
    
def compile_file(file, output):
    try:
        py_compile.compile(file, output, doraise=True)
        c = SuccessfullyCompile()
    except Exception as e:
        print('COMPILER : COMPILE ERROR')
        c = CompileError()
        c.errormsg = str(e)

    return c

def file_to_here(file):
    f1 = open(file, 'r')
    fname = open('id.txt', 'r').read()
    f2=open(f'{fname}.py', 'w')
    shutil.copyfileobj(f1, f2)
    fname = int(fname)
    fname += 1
    fd = open('id.txt', 'w')
    fd.truncate(0)
    fd.write(str(fname))
    fd.flush()
    fd.close()
    fname -= 1
    return f'{fname}.py', fname

def compile_proc(file, statobj: Status, updater, stop_proc):
    _is = isinstance
    try:
        fd_name = file_to_here(file)
    except Exception:
        statobj.statusmsg = 'Failed to dump file to current path!'
        statobj.status = SystemException()
        statobj.kind = SystemException()
        updater(statobj)
        stop_proc(statobj)
        return -1
    statobj.statusmsg = 'Copied & Compiling...'
    statobj.status = Compiling()
    updater(statobj)
    r = compile_file(fd_name[0], '%d.pyc' % fd_name[1])
    if _is(r, CompileError):
        statobj.statusmsg = r.errormsg
        statobj.status = r
        statobj.kind = r
        updater(statobj)
        stop_proc(statobj)
        return -1
    return '%d.pyc' % fd_name[1]
    

update_interpreter()
