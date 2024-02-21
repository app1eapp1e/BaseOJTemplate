"""The best name for this module is stats.py, both for statistics and status.
"""
import qloader
class Status:
    def __init__(self):
        self.status = None
        self.kind = None
        self.rank = 0
        self.statusmsg = ''
        self.pointdata = []
        self.user = USER

def log_warn(txt):
    print('[-] Status.Warning:', txt)

class PointData:
    kind = None
    rank = 0

def storage_string_format(stat):
    d = {}
    d['kind'] = stat.kind.__class__.__name__
    d['rank'] = stat.rank
    d['pt'] = []
    d['user'] = stat.user
    for p in stat.pointdata:
        d1 = {}
        d1['kind'] = p.kind.__class__.__name__
        d1['rank'] = p.rank
        d['pt'].append(d1)
    return repr(d)

def search_for_class(name):
    return globals()[name]

def load_stat_format(string):
    data = eval(string)
    s = Status()
    s.kind = search_for_class(data['kind'])()
    s.rank = data['rank']
    try:
        s.user = data['user']
    except KeyError:
        s.user = 'Nobody'
    l = data['pt']
    for p in l:
        kind = search_for_class(p['kind'])()
        rank = p['rank']
        _p = PointData()
        _p.kind = kind
        _p.rank = rank
        s.pointdata.append(_p)
    return s

def get_stat_context(question_name):
    return open(get_stat_file_name(question_name), 'r').read()

def can_get_info(qid):
    try:
        calculate_ac_rate(get_stat_context(qloader.get_question_name(qid)))
        return True
    except Exception:
        return False

def calculate_ac_rate(stat_context):
    stats = stat_context.rstrip(' | ').split(' | ')
    total = len(stats)
    ac = 0
    for s in stats:
        f = load_stat_format(s)
        if f.kind.__class__ == Accepted:
            ac += 1
    return ac / total

def calculate_distribution(stat_context):
    stats = stat_context.rstrip(' | ').split(' | ')
    total = len(stats)
    ac = 0
    pa = 0
    ce = 0
    wa = 0
    rte = 0
    tle = 0
    uke = 0
    for s in stats:
        f = load_stat_format(s)
        if f.kind.__class__ == Accepted:
            ac += 1
        elif f.kind.__class__ == PartialAccepted:
            pa += 1
        elif f.kind.__class__ == CompileError:
            ce += 1
        elif f.kind.__class__ == WrongAnswer:
            wa += 1
        elif f.kind.__class__ == RTError:
            rte += 1
        elif f.kind.__class__ == TimeLimitExceeded:
            tle += 1
        else:
            uke += 1
    return {'total': total,
            'Accepted': ac,
            'Partial Accepted': pa,
            'Compile Error': ce,
            'Wrong Answer': wa,
            'Runtime Error': rte,
            'Time Limit Exceeded': tle,
            'Unknown reason': uke
            }

def load_multi_stat(qid):
    filename = get_stat_file_name(qloader.get_question_name(qid))
    context = open(filename, 'r').read()
    stats = context.rstrip(' | ').split(' | ')
    return [load_stat_format(s) for s in stats]
    

def add_stat(question_name, stat):
    fname = './questions/%s Stats.txt' % question_name
    fd = open(fname, 'a')
    fd.write(storage_string_format(stat))
    fd.write(' | ')
    fd.flush()
    fd.close()

def get_stat_file_name(question_name):
    return './questions/%s Stats.txt' % question_name

def recreate_stats():
    l = qloader.qlist
    for q in l:
        fd = open(get_stat_file_name(q), 'a')
        fd.close()

class CompileError:
    errormsg=''

class PartialAccepted:
    pass

class Accepted:
    pass

class SystemException:
    pass

class WrongAnswer:
    pass

class RTError:
    pass

class SuccessfullyCompile:
    pass

class TimeLimitExceeded:
    pass

class SpecialJudgement:
    pass

### STATUS KINDS

class Compiling:
    pass

class Judging:
    pass

class Finished:
    pass

USER = 'Nobody'
def setuser(u):
    global USER
    USER = u
recreate_stats()
