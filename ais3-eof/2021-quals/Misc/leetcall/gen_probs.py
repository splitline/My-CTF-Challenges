import json
from secrets import token_urlsafe
from random import sample, randint

problems = [
    {
        "id": 1,
        "title": "Hello",
        "description":
            "Write a code that takes a name as an input and print out a greeting with that name.\n"
            "The greeting format should be 'Hello, <name>!'",
        "sample_input": ["Alice", "Bob"],
        "sample_output": ["Hello, Alice!", "Hello, Bob!"],
        "test_cases": [
            ["Alice", "Hello, Alice!"],
            ["Alice\nBob", "Hello, Alice!\nHello, Bob!"]
        ],
        "length_limit": 128,
    },
    {
        "id": 2,
        "title": "Fibonacci",
        "description":
            "Write a code that takes a number as an input and print out the nth Fibonacci number. (1 ≤ n ≤ 70)\n"
            "The fibonacci sequence is defined as: F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1.",
        "sample_input": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        "sample_output": ['1', '1', '2', '3', '5', '8', '13', '21', '34', '55'],
        "test_cases": [
            ['1\n2\n3\n4\n5\n6\n7\n8\n9\n10',
                '1\n1\n2\n3\n5\n8\n13\n21\n34\n55'],
        ],
        "length_limit": 256,
    },
    {
        "id": 3,
        "title": "FizzBuzz",
        "description":
            "Write a code that just print out fizzbuzz sequence for numbers from 1 to 10000. (split each output with a newline character)\n"
            'The fizzbuzz sequence is defined as: "FizzBuzz" if the number is divisible by 3 and 5, "Fizz" if the number is divisible by 3, "Buzz" if the number is divisible by 5, and the number itself otherwise.',
        "sample_input": ['(N/A, no stdin in this problem)'],
        "sample_output": ['1\n2\nFizz\n4\nBuzz\n...\n...\n9998\nFizz\nBuzz'],
        "test_cases": [
            ['',
                '\n'.join(map(
                    lambda i:
                    "Fizz"*(i % 3 == 0)+"Buzz" * (i % 5 == 0) or str(i),
                    range(1, 10001)
                ))]
        ],
        "length_limit": 512,
    }
]

names = [token_urlsafe(randint(1, 16)) for _ in range(500)]
problems[0]['test_cases'].append([
    '\n'.join(names),
    "\n".join(f"Hello, {name}!" for name in names)
])

for n in [20, 40, 60]:
    nums = sample(range(1, 71), n)
    problems[1]['test_cases'].append([
        '\n'.join(map(str, nums)),
        '\n'.join(
            map(lambda n: str(pow(2 << n, n+1, (4 << 2*n)-(2 << n)-1) %
                (2 << n)), nums)
        )
    ])

json.dump(problems, open('share/problems.json', 'w'))
