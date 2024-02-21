import compiling_py, status
from status import *
import func_timeout
import io
import subprocess
import os
import sys
import importlib

ios = [sys.stdin, sys.stdout, sys.stderr]

class LoadedKey:
    def __init__(self, data):
        self.data = data
        # data was structured in [[i1, o1], [i2, o2], ...]
        self.pvalue = 100 // len(self.data)

    def cmp(self, inputid, output):
        answer = self.data[inputid][1]
        response = '\n'.join([s.lstrip().rstrip() \
                              for s in output.splitlines()])
        if answer == response:
            return True
        else:
            return False

@func_timeout.func_set_timeout(1.01)
def get_output(interpreter, pycname, inputdat, args=[]):
    os.chdir(os.path.dirname(__file__))
    _f = open('__input__', 'a')
    _f.truncate(0)
    _f.write(inputdat)
    _f.flush()
    _f.close()
    PIPE = subprocess.PIPE
    # pycname = os.path.join(os.path.dirname(__file__), pycname)
    with open('__input__', 'r') as file:
        module = os.path.splitext(pycname)[0]
        old_stdin = sys.stdin
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        new_stdout = io.StringIO()
        new_stderr = io.StringIO()
        sys.stdin = file
        sys.stdout = new_stdout
        sys.stderr = new_stderr
        try:
            try:
                module_spec = importlib.util.find_spec(module)
                module_loaded = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module_loaded)
            except SystemExit:
                pass
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            if len(new_stderr.getvalue()) == 0:
                return new_stdout.getvalue()
            else:
                return RTError()
        except Exception as e:
            sys.stdin = old_stdin
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return RTError()
    
    

def judge_proc_py(file, statobj: Status, updater, stop_proc, load_key,
                  spjmod=None):
    os.chdir(os.path.dirname(__file__))
    existspj = not (spjmod == None)
    _is = isinstance
    exename = compiling_py.compile_proc(file, statobj, updater, stop_proc)
    if exename==-1:
        updater(statobj)
        return
    statobj.status = Judging()
    updater(statobj)
    inputid = 0
    has_ac = False
    has_error = False
    all_rte = True
    all_tle = True
    for i, o, spj in load_key.data:
        do_cmp = True
        p = PointData()
        try:
            output = get_output(compiling_py.PYTHON, exename, i, [])
            if _is(output, RTError):
                p.kind = RTError()
                all_tle = False
                do_cmp = False
                
            if do_cmp:
                if not spj:
                    correct = load_key.cmp(inputid, output)
                    if correct:
                        all_rte = False
                        all_tle = False
                        has_ac = True
                        p.rank = load_key.pvalue
                        statobj.rank += load_key.pvalue
                        p.kind = Accepted()
                    else:
                        all_rte = False
                        all_tle = False
                        has_error = True
                        p.rank = 0
                        p.kind = WrongAnswer()
                elif existspj:
                    p.kind = SpecialJudgement()
                    p.rank = spjmod.special_judge(load_key.data[inputid][1],
                                                  output, load_key.pvalue)
                    statobj.rank += p.rank
                    if p.rank == load_key.pvalue:
                        all_rte = False
                        all_tle = False
                        has_ac = True
                        p.kind = Accepted()
                    else:
                        has_error = True
        except func_timeout.exceptions.FunctionTimedOut:
            sys.stdin = ios[0]
            sys.stdout = ios[1]
            sys.stderr = ios[2]
            all_rte = False
            has_error = True
            p.kind = TimeLimitExceeded()
        statobj.pointdata.append(p)
        inputid += 1
        
    if all_rte:
        statobj.kind = RTError()
    elif all_tle:
        statobj.kind = TimeLimitExceeded()
    elif not has_error and has_ac:
        statobj.kind = Accepted()
    elif not has_ac and has_error:
        statobj.kind = WrongAnswer()
    else:
        statobj.kind = PartialAccepted()
    statobj.status = Finished()
    updater(statobj)
    
