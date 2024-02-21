"""More wrappings for the OJ library.
The functions are used in UI demo, but not imported from here"""

import os
from qloader import *
from status import *

def pathinit():
    os.chdir(os.path.dirname(__file__))

def legal_language(lang):
    return lang.capitalize() in ['C', 'C++', 'Python', 'Pascal']

help_info = '''I. ABOUT THE CORE
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
'''

def get_spj(qid):
    try:
        spjmod = __import__('questions.%s' % qlist[qid])
        spjmod = getattr(spjmod, qlist[qid])
        return spjmod
    except Exception:
        return None

def question_ac_rate(qid):
    return calculate_ac_rate(
                    get_stat_context(
                        get_question_name(qid)))

def question_distribution(qid):
    return calculate_distribution(
                    get_stat_context(
                        get_question_name(qid)))
