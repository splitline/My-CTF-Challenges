import sys

# Delete all imported modules
for name in list(sys.modules.keys()):
    # '_bootlocale' is for open()
    # if encoding of `open` is not specified, it will automatically import `_bootlocale` to get the default encoding
    if name != '_bootlocale':
        del sys.modules[name]


def hook(event, args):
    """
    Using Python runtime audit hooks to prevent exec / eval normal python codes.
    audithook:
    - https://www.python.org/dev/peps/pep-0578/
    - https://docs.python.org/3/library/audit_events.html
    """
    if event not in ('open', 'builtins.input', 'builtins.input/result'):
        raise Exception("Bad event: " + event+"\n"+str(args))
    if event == 'open' and args[0] != 0:
        raise Exception("Sandbox only accepts stdin from file 0")


sys.addaudithook(hook)
del sys, hook

# Your code starts here
{code}
