# CLAIM: QID = Question ID
qlist = []

def update_qlist():
    global qlist
    qlist = open('./questions/qlist.txt', 'r').read().splitlines()

def seek_for_qid(n):
    try:
        
        name = qlist[n]
    except IndexError:
        raise IndexError('Bad Question ID')
    try:
        data = eval(open('./questions/%s.txt' % name, 'r').read())
    except Exception:
        raise Exception('Question Loading Failure')
    return data

def get_question_name(n):
    try:
        name = qlist[n]
    except IndexError:
        raise IndexError('Bad Question ID')
    return name

update_qlist()
