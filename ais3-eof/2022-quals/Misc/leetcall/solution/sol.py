# Maybe not the best solution but it works (?)


# Challenge 1: Hello
def hello():
    # list(map(print, map("Hello, {}!".format,  open(0).read().splitlines() )))
    list(map(print, map(getattr("Hello, {}!", 'format'), getattr(getattr(open(0), 'read')(), 'splitlines')())))


# Challenge 2: Fibonacci
def fibonacci():
    # map(print,
    #     map(round,
    #         map(float.__truediv__,
    #             map(float.__pow__, iter(1.618033988749895.__float__, 0),
    #                 map(int, open(0).read().splitlines())),
    #             iter((pow(5, .5)).__float__, 0))
    #         )
    #     )
    list(map(print,map(round,map(getattr(float,'__truediv__'),map(getattr(float,'__pow__'),iter(getattr(1.618033988749895,'__float__'),0),map(int,getattr(getattr(open(0),'read')(),'splitlines')())),iter((getattr(pow(5,.5),'__float__')),0)))))


# Challenge 3: FizzBuzz
def fizzbuzz():
    # list(map(
    #     print,
    #     map("{[0]}".format,
    #         map(str.split,
    #             map("".join,
    #                     zip(
    #                         ['', '', 'Fizz'] * 3334,
    #                         ['', '', '', '', 'Buzz'] * 2000,
    #                         iter(" ".__str__, 0),
    #                         map(str, range(1, 10001))
    #                     )
    #                 )
    #             )
    #         )
    # ))
    list(map(print, map(getattr("{[0]}", "format"), map(getattr(str, "split"), map(getattr("", "join"), zip(getattr(getattr("||Fizz", "split")("|"), "__mul__")(3334), getattr(getattr("||||Buzz", "split")("|"), "__mul__")(2000), iter(getattr(" ", "__str__"), 0), map(str, range(1, 10001))))))))


