# AIS3 2021 Pre-Exam [Reverse]

## 🐰 Peekora 🥒

- Category: Reverse
- Difficulty: Easy
- Solves: 75/327 (Pre-Exam), 0/190 (MyFirstCTF)
- Keywords: Pickle Bytecode

其實這題只是讀 bytecode 練習題而已，並告訴大家可以用 pickle 寫程式 —— 然而就算讀不懂（甚至不 disassemble 它），多少也有辦法通靈得出來。但其實除了硬讀以外，還有一些不用花苦力讀的有趣解法，可惜的是好像沒看到什麼人用 XD

### Solution 0x01

```
$ python3 -m pickletools -a flag_checker.pkl
```
然後硬讀，讀不懂的就爆破，沒了。

99% 的人都是這麼做的。

### Solution 0x02

簡單看過 bytecode 可以看出它先用 `input` 讀入輸入，再用 `__getitem__` 取出各個字元後用 `__eq__` 之類的東西逐一比對字元。

好，夠了，知道這些資訊就可以不用繼續讀了。

我們可以把 `__builtins__.input` 改成自己的 function，讓它吐回一個假的 str，其中那個假的 str 自訂了 `__eq__` 等方法的邏輯，讓 pickle 在用 `__eq__` 比對的同時，也順便幫你把正確的 flag 填回去，等 pickle load 完 flag 也出來了。詳情請見 [solve.py](Peekora/solve.py)。

### Solution 0x03

既然知道只要比對錯一個字元就會觸發 `exit`，那就可以透過這個特性 hook 住 `__builtins__.exit` 藉此爆破出所有字元了。
