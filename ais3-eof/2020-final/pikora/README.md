# Pikora

- Category: Misc
- Static Score: 500 / 500
- Solves: 1 / 25

## Solution

就只是了解 pickle 序列化的運作原理然後開寫而已，樸實無華的 PPC 題 XD

我想網路上各路大神的 PVM (pickle VM) 介紹應該都已經相當不錯了，這邊就不多提。比較值得一提的點大概是，由於 PVM 只是一個純粹的 stack machine，沒有類似於 condition、loop 的功能，能做到事情只有基礎的 call function 和 assignment，因此需要透過有點類似 functional programming 的技巧來幫助你解題，例如活用 `map`、`itertools` 等等。

這邊提供一下我的個人解法：

1. Warmup (Length Limit: 30)
    ```python
    b'(VPeko!!!\ni__builtin__\nprint\n.'
    ```

2. A+B Problem (Length Limit: 333)
    ```python
    b"c__builtin__\ngetattr\np0\n0c__builtin__\nint\np1\n0c__builtin__\nmap\np2\n0(g2\n(c__builtin__\nprint\ncitertools\nstarmap\n(g0\n(g1\nV__add__\ntRg2\n(cfunctools\npartial\n(g2\ng1\ntRg2\n(g0\n(c__builtin__\nstr\nVsplit\ntRg0\n(g0\n(c__builtin__\nopen\n(I0\ntRVread\ntR(tRVsplitlines\ntR(tRtRtRtRtRi__builtin__\nlist\n."
    ```

    Pseudocode:
    ```python
    list(map(print,
        itertools.starmap(int.__add__, 
            map(functools.partial(map, int), 
                map(str.split, open(0).read().splitlines())
            )
        )
    ))
    ```

    **非預期解**
    這題由於每筆測資的數量都是固定的，而且並不多，於是 @sasdf 就直接 brute force 試岀有幾筆測資 —— 只要一直複製貼上單次 A+B 計算的 bytecode 直到符合測資數量即可 AC，並不需要實作類似迴圈的行為。

3. Leap Year (Length Limit: 1024)
    ```python
    b"c__builtin__\ngetattr\np0\n0c__builtin__\nint\np1\n0c__builtin__\nmap\np2\n0c__builtin__\niter\np3\n0c__builtin__\nlist\np4\n0g4\n(g2\n(g1\ng0\n(g0\n(c__builtin__\nopen\n(I0\ntRVread\ntR(tRVsplitlines\ntR(tRtRtRp5\n0g0\n(g1\nV__mod__\ntRp6\n0g3\n(g0\n(I0\nV__int__\ntRI1\ntRp7\n0g2\n(g0\n(g1\nV__eq__\ntRg2\n(g6\ng5\ng3\n(g0\n(I400\nV__int__\ntRI1\ntRtRg7\ntRp8\n0g2\n(g0\n(g1\nV__eq__\ntRg2\n(g6\ng5\ng3\n(g0\n(I4\nV__int__\ntRI1\ntRtRg7\ntRp9\n0g2\n(g0\n(g1\nV__ne__\ntRg2\n(g6\ng5\ng3\n(g0\n(I100\nV__int__\ntRI1\ntRtRg7\ntRp10\n0g4\n(g2\n(c__builtin__\nprint\ng2\n(g0\n((VNormal'\nVLeap'\nlV__getitem__\ntRg2\n(g0\n(g1\nV__or__\ntRg2\n(g0\n(g1\nV__and__\ntRg9\ng10\ntRg8\ntRtRtRtR."
    ```

    Pseudocode:
    ```python
    data = list(map(int, open(0).read().splitlines()))
    mod = int.__mod__

    # year % 400 == 0
    cond1 = map(int.__eq__, 
            map(mod, data, iter((400).__int__, 1)),
            iter((0).__int__, 1)
        )

    # year % 4 == 0
    cond2 = map(int.__eq__, 
            map(mod, data, iter((4).__int__, 1)),
            iter((0).__int__, 1)
        )

    # year % 100 != 0
    cond3 = map(int.__ne__, 
            map(mod, data, iter((100).__int__, 1)),
            iter((0).__int__, 1)
        )

    list(map(print,
        map(["Normal", "Leap"].__getitem__,
            map(int.__or__,
                map(int.__and__, cond2, cond3),
                cond1
            )
        )
    ))
    ```