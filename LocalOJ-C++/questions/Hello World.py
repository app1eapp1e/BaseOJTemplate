def special_judge(answer, response, full):
    response = '\n'.join([s.lstrip().rstrip() \
                              for s in response.splitlines()])
    if answer == response:
        return full
    elif answer in response:
        return full // 5 * 4 # 80%
    elif response in answer:
        return full
    else:
        return 0
