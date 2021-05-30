import pickle
import pickletools


class fake_str:
    def __init__(self):
        self._str = []

    def startswith(self, a):
        print("str.startswith:", a)
        return True

    def endswith(self, a):
        print("str.endswith:", a)
        return True

    def __getitem__(self, index):
        return self._str[index]


class fake_chr():
    def __init__(self, char=None):
        self.char = char

    def __eq__(self, target):
        if type(target) == fake_chr and self.char != None:
            target.char = self.char
        else:
            self.char = target
        return True

    def __str__(self):  # for debug usage
        return "<chr: (ch=%s)>" % (self.char)


if __name__ == "__main__":
    fake_flag = fake_str()

    # Generate AIS3{<fake_chr><fake_chr>...}
    for i, ch in enumerate("AIS3{"):
        fake_flag._str.append(fake_chr(ch))
    for i in range(len("AIS3{"), 20):
        fake_flag._str.append(fake_chr())

    __builtins__.input = lambda _: fake_flag # hook __builtins__.input

    pkl = open("flag_checker.pkl", 'rb').read()
    pickle.loads(pkl)

    flag = ''

    for i, ch in enumerate(fake_flag._str):
        print(ch)
        if type(ch.char) == fake_chr:
            flag += ch.char.char
        elif type(ch.char) == str:
            flag += ch.char
        elif ch.char == None:  # no more chars
            flag += "}"
            break
        else:
            raise "should not happen"

    print("FLAG:", flag)
