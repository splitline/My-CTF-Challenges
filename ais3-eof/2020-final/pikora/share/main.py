#!/usr/local/bin/python3
import epicbox
from random import randint
import base64

epicbox.configure(profiles=[epicbox.Profile('python', 'python:3.9-alpine')])


def challenge(title, question, example_input, example_output, testcases, len_limit):
    print(title)
    print(question, end='\n\n')
    print("Example Input: \n", example_input, sep='', end='\n\n')
    print("Example Output: \n", example_output, sep='', end='\n\n')
    print('-'*32)
    print("Pickle Length Limit (after base64 decoded):", len_limit)
    try:
        pickle_code = base64.b64decode(input("Your base64 encoded pickle code: "))
    except ValueError:
        print("b64decode failed!")
        exit(1)

    if len(pickle_code) > len_limit:
        print('[30cm] Length Limit Exceeded')
        exit(1)

    script = f'''
import sys
import _pickle
pickle_file = open('./pickle_code', 'rb')

def hook(event, arg):
    if event not in ['pickle.find_class','open','builtins.input','builtins.input/result']:
        raise Exception(f'audithook: Event {{event}} is not in whitelist.')
    if event == 'open' and arg[0] != 0:
        raise Exception("audithook: Bad open file.")

sys.addaudithook(hook)
del hook

_pickle.load(pickle_file)
'''
    for i, (input_, answer) in enumerate(testcases):
        files = [{'name': 'main.py', 'content': script.encode('utf-8')},
                 {'name': 'input', 'content': input_.encode('utf-8')},
                 {'name': 'pickle_code', 'content': pickle_code}]
        limits = {'cputime': 3, 'memory': 512}
        res = epicbox.run('python', 'python3 main.py < input', files=files, limits=limits)
        # print(res)
        if not (res['exit_code'] is not None and not res['exit_code']):
            print("[\|/] Runtime Error")
            exit(1)

        if res['stdout'].decode('utf-8').strip() != answer.strip():
            print("[❎] Wrong Answer")
            exit(1)

        print(f"=== STAGE {i+1} CLEARED ===", flush=True)
    print('[✅] AC, Congrats! \n\n')


if __name__ == '__main__':
    print(
        """
Pickle oriented programming! Let's play with pickle 🥒.
We have 3 easy-peasy problems (well, if you write in normal python) here, just conquer them all and get the flag!

By the way, there are some limitations for preventing cheating solutions.
For example, you can't use eval, exec, os module, and can't create a code/function object neither.

For more information, please refer to the provided `public.py`, happy pickling!

Note: This is just a pure PPC challenge, NOT a sandbox escape challenge at all. But if you insist… feel free to try it :p
    """
    )

    challenge(
        '[Warmup] (1/3)',
        'There is no input, what you need is just to print `Peko!!!`.',
        '(N/A)', 'Peko!!!', [['', 'Peko!!!']], 30)

    testcases = []

    for i in range(5):
        in_group = []
        out_group = []
        for _ in range(10):
            a = randint(1, pow(100, i+1))
            b = randint(1, pow(100, i+1))
            in_group.append(f'{a} {b}')
            out_group.append(f'{a+b}')
        testcases.append(['\n'.join(in_group), '\n'.join(out_group)])

    challenge(
        '[A+B Problem] (2/3)',
        'Each line would contain 2 numbers A and B, and you should print the result of A+B.',
        '1 1\n8 9\n55 66', '2\n17\n121', testcases, 333)

    testcases = [
        []  # random
        ['', ''],  # normal
        ['', ''],  # leap
    ]

    import calendar
    for y in range(1582, randint(1900, 2021)):
        if calendar.isleap(y):
            testcases[2][0] += f'{y}\n'
            testcases[2][1] += f'Leap\n'
        else:
            testcases[1][0] += f'{y}\n'
            testcases[1][1] += f'Normal\n'

    test_in = []
    test_out = []
    for i in range(30):
        y = randint(2021, 3000)
        test_in.append(f'{y}')
        test_out.append('Leap' if calendar.isleap(y) else 'Normal')
    testcases[0] = ['\n'.join(test_in), '\n'.join(test_out)]

    challenge(
        '[Leap Year] (3/3)',
        '''
Each line contains only one input YEAR, and you need to check if it is a leap year.
If it is, you should print `Leap`, otherwise you should print `Normal`.
    '''.strip(),
        '2020\n2019\n1900', 'Leap\nNormal\nNormal', testcases, 1024)

    print('FLAG: AIS3{U_r_R3a11y_a_pick1e_K!ng,peko!}')
