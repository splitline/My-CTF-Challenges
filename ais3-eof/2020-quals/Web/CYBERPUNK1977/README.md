# Cyberpunk 1977

- Category: Web
- Solves: 8 / 95 (scores >= 1), 55 (scores > 1)

## Solution

總共有四個關卡：
0. 挖到 source code
1. SQL Quine
2. 繞過 token 限制
3. Leak secret_key & 偽造 session

### 挖到 source code

> /hint?file=hint.txt

hint 中提到了以下兩點
- I use `tiangolo/uwsgi-nginx-flask` to build this cool stuff. (with default configuration)
- [VISUAL BASIC 2077](https://drive.google.com/file/d/1AXEcUSwGlBON_1abv919AIw5CSX2I5VU/view)

還順帶了一個送分的任意讀檔，但不能讀 `*.py`，但沒關係，我們可以讀 `.pyc`。

`uwsgi` 的行為是會把 python 當 module import 進來，因此會在 `__pycache__` 底下產生 pyc，而 pyc 的格式是這樣的：`{script_name}.{interpreter}-{py_version}.pyc`。根據該 image 在 [Dokcer Hub](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/) 上面的敘述可以看到支援的 python 版本，以及使用 `main.py` 作為範例，逐一嘗試便可以讀取到 `__pycache__/main.cpython-38.pyc`。

> 註：我並沒有預期大家一定要知道這個環境下有 `__pycache__` 這個東西的存在，但預期上是只要自己用這個 image 跑一個東西起來之後應該就會發現它了。

接下來就丟給 decompiler (e.g. uncompyle6) 還原出原始碼即可，但小心，decompiler 可能會騙你ㄛ。

### SQL Quine

去看我的 exploit 啦，這邊就只是寫扣而已，有很多種寫法 XD

比較值得提的的就兩點：
- `/**/` 可以當空白用
- `X'22'` = `CHAR(0x22)` 

### 繞過 token 限制
成功登入之後，必須讓 token 是 `ADMIN-E864E8E8F230374AA7B3B0CE441E209A` 才能有機會看到 flag：
```python
if token.upper() == "ADMIN-E864E8E8F230374AA7B3B0CE441E209A":
    return ("Hello, " + username + " ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡  Here is your flag: {flag}").format(flag=flag)
else:
    return ("Hello, " + username + " ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡  No flag for you (´;ω;`)")
```

但問題是在最開始的時候就會有一個檢測，如果你的 username 不是 `admin` 但被 regex 搜到 token 裏有 `ADMIN` 就會噴掉：
```python
if username != "admin" and re.search("ADMIN", token, re.I | re.A):
    return "Hey {username}, admin's token is not for you (・へ・)".format(username=username)
```
雖然讓 username 變 admin 不難沒錯，但我們還需要利用到裏頭的那個 format string 漏洞來 leak 出 secret_key 啊，這步驟一定要能自由控制 username 才能做到。

不過可以注意到，程式是用 `token.upper()` 去比對的，`upper` 會不會有什麼魔法呢？這個可以很簡單的 fuzz 出來：

```python
for i in range(0x10FFFF):
    if chr(i) != chr(i).upper() and chr(i).upper() in string.ascii_uppercase:
        print(i, chr(i), chr(i).upper())
```
排除小寫字元，有這些酷炫字元有神奇的特性
```
305 ı I
383 ſ S
64261 ﬅ ST
64262 ﬆ ST
```
而 `305 ı I` 正是我們需要的，可以把它拿來取代 `ADMIN` 的 `I`，最後我們可以得到這樣的 payload：
```
ADMıN-E864E8E8F230374AA7B3B0CE441E209A
```

### Leak secret_key & 偽造 session

進入最後階段了，我們必須把 session 中的 is_admin 改成 True 才能看到 flag，因此我們要想辦法偽造 session。

這邊有一個明顯的 format string 洞：
```python
return ("Hello, " + username + " ｡:.ﾟヽ(*´∀`)ﾉﾟ.:｡  Here is your flag: {flag}").format(flag=flag)
```
我們可以搭配前面的 SQL Quine，把 username 設定為 `{flag.__str__.__globals__[app].secret_key}` 就能撈到 secret_key 了，不過還是來稍微講一下原理好了。

`flag` 是一個 Flag object，而其的原型是這樣的
```python
class Flag():
    def __str__(self):
        if session.get('is_admin', False):
            return getenv("FLAG", 'FLAG{F4K3_FL4G}')
        else:
            return "Oops, You're not admin (・へ・)"
```
它的底下有一個 `__str__` method，而在 python 中每一個自訂的 function 都會有一個 `__globals__` dict 來儲存那個 function 有權限存取到的所有 global 變數。而對於我們的那個 `flag` object 而言，他的全域變數當然包含了 `app = Flask(__name__)`，接著就能理所當然的讀到 `app` 底下的 `app.secret_key` 了。

有了 `secret_key` 我們就能輕鬆偽造 session 了，有很多方法能做這件事，網路上也有很多人寫腳本幫你簽 session 了，不過我是選擇自己寫一個 MockApp 啦，個人是覺得這樣比較酷炫。

一步到位的完整流程就去看我的 exploit 腳本吧。

## Postscript

話說，不知道如果這題不是作業的 revenge 題的話，難度會是多少 XD？
