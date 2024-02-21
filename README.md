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