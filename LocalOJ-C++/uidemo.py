import os
os.chdir(os.path.dirname(__file__))

import colorama
from judge_cpp import *
from judge_c import *
from judge_py import *
from judge_pascal import *
from qloader import *
from status import *
colorama.init()
JUDGING_ID = None

def stop_proc(status):
    print('[-] Judgement Terminated.')

def updater(status):
    _is = isinstance
    print('[*] Judgement Update')
    if _is(status.status, SystemException):
        print('[-] System Exception!')
    elif _is(status.status, Compiling):
        print('[*] Compiling...')
    elif _is(status.status, Judging):
        print('[*] Judging...')
    elif _is(status.status, CompileError):
        print('[-] Compile Error')
        print('[-] Compiler output:')
        print(status.statusmsg)
        add_stat(get_question_name(JUDGING_ID), status)
    elif _is(status.status, Finished):
        print('[+] Finished')
        print('######################################################')
        print('Result: %s' % status.kind.__class__.__name__)
        print('Rank: %s' % status.rank)
        curr = 1
        print('TestNode ID\tResult\t\t\t\t\tRank')
        for data in status.pointdata:
            print('%s\t\t%s\t\t\t\t%s' % (curr, data.kind.__class__.__name__,
                                        data.rank)
                  )
            curr += 1
        add_stat(get_question_name(JUDGING_ID), status)

def stat_view(stats, qid):
    pg = 'a'
    while True:
        if pg=='a':
            print(
                '************* SUBMISSIONS FOR QUESTION #%d *************'%qid
                )
            i = 0
            for st in stats:
                print('%s\t%s\t\t%s\t( By %s )' % (i, st.rank,
                                        st.kind.__class__.__name__, st.user))
                i += 1
        elif pg=='s':
            try:
                ind = int(input('Single Submission # > '))
                stat = stats[ind]
                print('######################################################')
                print('Result: %s' % stat.kind.__class__.__name__)
                print('Rank: %s' % stat.rank)
                curr = 1
                print('TestNode ID\tResult\t\t\t\t\tRank')
                for data in stat.pointdata:
                    print('%s\t\t%s\t\t\t\t%s' % (curr, data.kind.__class__.__name__,
                                                data.rank)
                          )
                    curr += 1
            except Exception as e:
                print('[-] %s' % e)
        elif pg=='q':
            return
        else:
            print('[-] Try again')
        pg = input('A(ll submissions)/S(ingle submission)/Q(uit) > ').lower()

def judge(answer, spjmod):
    language = input('Language > ')
    language = language.capitalize()
    if language not in ['C', 'C++', 'Python', 'Pascal']:
        return
    file = input('Judge file > ')
    try:
        text = open(file, 'r').read()
        print('Preview:')
        print(text)
        if input('Judge[Y/N] > ') in 'nN':
            return
        s = Status()
        if language == 'C++':
            judge_proc_cpp(file, s, updater, stop_proc, LoadedKey(answer),
                           spjmod)
        elif language == 'C':
            judge_proc_c(file, s, updater, stop_proc, LoadedKey(answer),
                         spjmod)
        elif language == 'Python':
            judge_proc_py(file, s, updater, stop_proc, LoadedKey(answer),
                          spjmod)
        elif language == 'Pascal':
            judge_proc_pascal(file, s, updater, stop_proc, LoadedKey(answer),
                              spjmod)
    except (IOError, FileNotFoundError) as e:
        print('[-] %s' % e)
        return
    
    
        
    

def flip():
    print(colorama.ansi.clear_screen())

def seek_back():
    print(colorama.Cursor.POS(1, 1))

def do_question(qid):
    global JUDGING_ID
    current_page = 'd'
    try:
        spjmod = __import__('questions.%s' % qlist[qid])
        spjmod = getattr(spjmod, qlist[qid])
        print('[+] Loaded SPJ')
    except Exception:
        print('No/Corrupt SPJ for this question')
        spjmod = None
    try:
        data = seek_for_qid(qid)
        answer = data[5]
    except:
        print('[-] Bad question ID')
        print('\a')
        return
    while True:
        print('******************* %s *******************' % qlist[qid])
        if current_page == 'd':
            print('* DESCRIPTION *')
            print(data[0])
        elif current_page == 'r':
            print('* INPUT REQUEST *')
            print(data[1])
            print('* OUTPUT REQUEST *')
            print(data[2])
        elif current_page == 'e':
            current = 0
            for demo in data[3]:
                print('* INPUT #%s *' % current)
                print(demo[0])
                print('* OUTPUT #%s *' % current)
                print(demo[1])
                current += 1
        elif current_page == 'h':
            print('* HINT *')
            print(data[4])
        elif current_page == 'q':
            return
        elif current_page == 'j':
            JUDGING_ID = qid
            judge(answer, spjmod)
        elif current_page == 's':
            if can_get_info(qid):
                print('* STATISTICS *')
                ac_rate = calculate_ac_rate(
                    get_stat_context(
                        get_question_name(qid)))
                print('AC Rate: %.2f%%' % (ac_rate*100))
                print('* DISTRIBUTION *')
                dist = calculate_distribution(
                    get_stat_context(
                        get_question_name(qid)))
                for key in dist:
                    print('%s%s%s\t\t%.2f%%' % (
                        key, ' ' * (40-len(key)),
                        dist[key], dist[key]/dist['total']*100))
            else:
                print('* INFO CANNOT ANALYZE *')
        elif current_page == 'u':
            try:
                stat_view(load_multi_stat(qid), qid)
            except Exception:
                print('[-] Submission loading failure')
            
        else:
            print('[-] Bad page')
            print('\a')
        current_page=\
        input(
            'Goto page: \
D(escription)/R(equest)/E(xample)/H(int)/S(tatistics)/J(udge)/Q(uit)/\
(s)U(bmission) > '
            ).lower()
                

def helpview():
    print('''I. ABOUT THE CORE
README: IMPORTANT
1. run the batch file first!!!
2. It only supports C/C++, Python!
3. Plsase set the paths in "gcc_path.txt", "g++_path.txt", and "pypath.txt"!!!

Advantages :)
1. Portable, Local, Net-Free
2. Stable.
3. Open-Source.
4. Single-file formatted question, with question pack compiler.
5. More connections to GUI(updater), internal web judge(stop_proc, to let the client stopping receiving message).
6. Consecuative service functions and clear factory function(judge_proc_*)

Disadvantages ^_^
1. No MLE, OLE, PE(Not a problem ^_^)
2. Non-accurate Program Running Time, needs your program to finish in about 0.9+ seconds instead of 1.00.(Better trainings for you!!!)
3. I/O Binding sometimes fails.(Especially in Python, but now it's safer!)
4. Only have Python, Pascal, C, and C++.(Other languages are just the same, add by yourself!)
5. No Competition-related Functions.

II. ABOUT THE UI DEMO
The program is pushed by single-letter commands.
It's a simple demo of our core.
The prompt is clear enough.
''')
    input('Press Enter to continue...')
    print('\n\n')
def mainview():
    firstq = 0
    
    while True:
        print('Questions')
        print('=======================================================')
        
        for x in range(firstq, firstq+10):
            try:
                print('%s\t%s' % (x, qlist[x]))
            except IndexError:
                pass
        next_command = input('F(lip to question ...)/D(o ...)/Q(uit)/H(elp) > ')
        if next_command in ['f', 'F']:
            try:
                firstq = int(input('Flip to > '))
            except (ValueError, EOFError):
                pass
        elif next_command in ['q', 'Q']:
            quit()
        elif next_command in ['d', 'D']:
            try:
                qid = int(input('Do > '))
                do_question(qid)
            except (ValueError, EOFError):
                pass
        elif next_command in ['h', 'H']:
            helpview()
        else:
            print('Try again')

print(colorama.ansi.set_title('OJ -- Offline Judge'))
setuser(input('User > '))
flip()
mainview()
