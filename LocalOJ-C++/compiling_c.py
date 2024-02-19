import os
from status import *
import shutil
import subprocess

FORMAT = '%s -O2 -w -fmax-errors=3 %s -lm -o %s.exe 2>./__output__'

def update_gcc():
    global GCC
    current = os.path.dirname(__file__)
    os.chdir(current)
    GCC = open('./gcc_path.txt', 'r').read()
    
def compile_file(file, output):
    os.chdir(os.path.dirname(__file__))
    fd = os.popen(FORMAT % (GCC, file, output))
    text = open('__output__', 'r').read()
    

    if 'error' in text:
        c = CompileError()
        c.errormsg = text
    else:
        c = SuccessfullyCompile()

    return c

def file_to_here(file):
    f1 = open(file, 'r')
    fname = open('id.txt', 'r').read()
    f2=open(f'{fname}.c', 'w')
    shutil.copyfileobj(f1, f2)
    fname = int(fname)
    fname += 1
    fd = open('id.txt', 'w')
    fd.truncate(0)
    fd.write(str(fname))
    fd.flush()
    fd.close()
    fname -= 1
    return f'{fname}.c', fname

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
    r = compile_file(fd_name[0], '%d' % fd_name[1])
    if _is(r, CompileError):
        statobj.statusmsg = r.errormsg
        statobj.status = r
        statobj.kind = r
        updater(statobj)
        stop_proc(statobj)
        return -1
    return '%d.exe' % fd_name[1]
    

update_gcc()
