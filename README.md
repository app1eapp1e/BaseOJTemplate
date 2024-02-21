# ABOUT IT
1. This is a simple OJ library, contains all the functions of program judging.<br>
2. The factory functions are in file `judge_*.py`, function names are `judge_proc_*`.
3. This program offers a UI demo. See the help pane to get some help about the core and the demo.
4. **REMEMBER: CHANGE THE PATHS IN THE 4 TXT FILES!!!!!!!**
**RUN THE LIBRARY INSTALLER!!**<br>
Library installation list:
   - func-timeout
   - colorama used by UI demo
5. (v2)Now we have Special judge. 
The special judge needs a Python file 
in the same folder of the questions
`./LocalOJ-C++/questions`. The Python file offers a function
`special_judge()`, takes output, answer and the full mark of the test data.
For an example, `hello world`'s might be this:
```python
def special_judge(answer, response, full):
    response = '\n'.join([s.lstrip().rstrip() \
                              for s in response.splitlines()])
    if answer == response:
        return full
    elif answer in response:
        return full // 5 * 4 # 80%
    elif response in answer:
        return full // 5 * 3
    else:
        return 0
```
This means, that, If your output is `hello world`, 
you will get full. But if your output is more than
`hello world`, and with something else, like, 
your answer is `hello world!`,
you can get 80% of your point. 
If you typed `hello`, `world`, 
etc. that contains in the `hello world`, you'll get 60%.
Otherwise, you'll get 0.<br>
Judge function will automatically turn the SPJ's full mark
into AC.<br>
GUI demo automatically detects the SPJ's existence.
## Question pack format
For an example:
```python
[
"""Goldbach said: Each even number >=4 can be divided into the sum of 2 primes.
Like, 4=2+2, 6=3+3, 8=3+5, etc.
Given the even number, Your task is to find the split plans, that let the first prime be the smallest and the second be the largest.
""",

"""One line, N, an even number >=4, in range long long[-(1<<63)~((1<<63)-1)].
""",
"""One line, P and Q, spaced, are primes, that bas the largest Q and smallest P, and P+Q=N.
""",
[[
"""20""",
"""3 17""",
]],
"""20=3+17=7+13, we select the smallest P=3, Q=17.""",
[["""30""","""7 23""", False],
["""9876""", """5 9871""", False],
["""78686""", """37 78649""", False],
["""67868768""", """7 67868761""", False],
["""7686876868866""", """5 7686876868861""", False]],
]
```
The format is a Python list, contains:
- description: string
- input format: str
- output format: str
- example data ([[i1, o1], [i2, o2], ...])
- hint: string
- test data ([[i1, o1, s1], [i2, o2, s2], ...])

detail:
1. i/o: str, input/output data
2. s: bool, needs SPJ

The example may looks like this in OJ:

***
# Problem description
Goldbach said: Each even number >=4 can be divided into the sum of 2 primes.
Like, 4=2+2, 6=3+3, 8=3+5, etc.
Given the even number, Your task is to find the split plans, that let the first prime be the smallest and the second be the largest.
# Input format
One line, N, an even number >=4, in range long long[-(1<<63)~((1<<63)-1)].
# Output format
One line, P and Q, spaced, are primes, that bas the largest Q and smallest P, and P+Q=N.
# Test input 1
20
# Test output 1
3 17
# hint
20=3+17=7+13, we select the smallest P=3, Q=17.