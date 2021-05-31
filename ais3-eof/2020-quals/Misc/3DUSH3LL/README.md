# 3DUSH3LL

- Category: Misc
- Solves: 0 / 95 (scores >= 1), 55 (scores > 1)

## Solution

### TL;DR
1. Get `<class 'function'>` from `(lambda:None).__class__`.
2. Get `<class 'code'>` from `(_ for _ in ()).gi_code.__class__`.
3. Use `class_function(class_code(args...), {})` to create arbitrary function.
4. Pwned!

### Detailed Solution

> 這篇 writeup 有點詳細到 tutorial 程度了 XD

顯然的，這是一個 Python sandbox，直接讓我們來看看 source code 吧，核心內容就是這一小段而已：
```python
for bad in ['mro', 'base', '__code__', '__subclasses__', '__dict__', 'import', 'builtins', 'module', 'attr', 'globals']:
            if bad in command:
                print(f"{bad}: Permission denied")
                break
        else:
            try:
                print(eval(command, {"__builtins__": {}}))
            except Exception:
                print(f'/bin/sh: {command}: not found')
```

總而言之，它用黑名單的方式禁止你輸入的內容出現以下的字串：

- `mro`
- `base`
- `__code__`
- `__subclasses__`
- `__dict__`
- `import`
- `builtins`
- `module`
- `attr`
- `globals`

通過上述黑名單之後，就會直接去 eval 你的輸入了，不過值得注意的是 [eval 的第二個參數](https://docs.python.org/3/library/functions.html#eval)被傳入了 `{"__builtins__": {}}`，這樣的行為導致 `__builtins__` 的內容被清空，而 `__builtins__` 中儲存的就是 Python 中常見的內建 function，如此一來像是 `exec`, `eval`, `open` 等等的 function 都不能直接使用了。

這樣的 python sandbox 環境可能會讓熟悉 web security 的人聯想到 Jinja2 SSTI，不過可惜的是經典 payload（e.g. `[].__class__.__base__.__subclasses__....`） 中必要的許多字詞都被擋掉了，也沒辦法使用 `__getattribute__` 的方法撈出各種屬性，我們只好另覓蹊徑。

這邊我使用的方法是直接透過 code object 以及 function object 來建構任意 function —— 嗯等等，或許有點跳太快了，回來聊聊我們在 Python 中定義一個 function 時到底發生了什麼吧。

事情是這樣的，我們知道 Python 中任何東西都是一個 object，就連 function 也不例外。那麼我們可以回頭想想，Python 呼叫一個 function 的時候到底是怎麼知道要執行什麼呢？總要有一個地方儲存嘛。像是參數、程式內容等等的東西，到底被擺在哪呢？直接讓我們來觀察一個 function 物件看看：

```python
>>> def meow(): pass
>>> dir(meow)
['__annotations__', '__call__', '__class__', '__closure__', '__code__', '__defaults__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__get__', '__getattribute__', '__globals__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__kwdefaults__', '__le__', '__lt__', '__module__', '__name__', '__ne__', '__new__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
>>> set(dir(meow)) - set(dir([]))
{'__globals__', '__call__', '__annotations__', '__code__', '__qualname__', '__closure__', '__dict__', '__get__', '__module__', '__defaults__', '__kwdefaults__', '__name__'}
```
看起來 function 比起其他的 object 多出很多 magic attribute，而其中有個值得注意的東西：`__code__`。

`__code__` 中儲存的就是 function 程式內容的一些基本資料，像是 byte code, constant, variable 等等，這邊簡單介紹一下它底下各個 attribute 的意義：

|解釋|`[*]`|
|-|-|
| 幾個參數 (int) | `co_argcount`|
| function 的 scope 內有幾個值 (int)  |`co_nlocals`|
| stack 開多大 (int) | `co_stacksize`|
| compile 的方式 (int) | `co_flags`|
| 你的 bytecode (bytes) | `co_code`|
| function 的 const 值 (tuple) | `co_consts` |
| function 有用到但不在 scope 裡的變數名稱 (tuple) |`co_names`|
| function 中 define 的變數名稱 (tuple)| `co_varnames`|
| 檔名 / `'<stdin>'`  |`co_filename`|
| function 名稱 (str) |`co_name`|
|第幾行開始的 (int) |`co_firstlineno`|
| 行號表 (bytes) |`co_lnotab`|

不過其實可以先不用管那麼多啦。其實，如果你要複製一個現成的 function 的話，只要照著把它 `__code__` 底下的各個 attribute 填入 code 建構子就好了，暫時不用管它的含義 XD，至於 argument 順序怎麼擺呢？我們可以直接透過 `help((lambda:None).__code__)` 看一下：
```
Help on code object:

class code(object)
 |  code(argcount, posonlyargcount, kwonlyargcount, nlocals, stacksize,
 |        flags, codestring, constants, names, varnames, filename, name,
 |        firstlineno, lnotab[, freevars[, cellvars]])
 |
 |  Create a code object.  Not for the faint of heart.
 |
 |  Methods defined here:
 | ...
```

Well, **not for the faint of heart**, ok fine, we don't care :).

至此，我們已經能順利建構一個 function 中的 code object（`__code__` 的部分）。

而建構完整的 function 就相對簡單很多了：
```
Help on class function in module builtins:

class function(object)
 |  function(code, globals, name=None, argdefs=None, closure=None)
 |
 |  Create a function object.
 |
 |  code
 |    a code object
 |  globals
 |    the globals dictionary
```

只要傳入兩個參數：code object 以及 globals 就行了。

總結一下，要從底層開始創造一個 function 要填這些東西：
```
function(
    code(argcount, posonlyargcount, kwonlyargcount, nlocals, stacksize,
        flags, codestring, constants, names, varnames, filename, name,
        firstlineno, lnotab),
    globals
)
```

因此，我們只要拿到
1. `class function(object)` 
2. `class code(object)`
3. code object 必要的 argument

就可以創造/複製出任意 function 了。

`class function(object)` 的部分比較簡單，可以透過 `(lambda:None).__class__` 的方式拿到。

`class code(object)` 由於 `__code__` 被擋，因此不能最直覺的在一個 function 底下拿到，那還有什麼地方會有 code object 呢？其實像是 `coroutine object` 或 `generator object` 等等的底下分別有 `cr_code` 跟 `gi_code` 可以利用，而在此場景下 generator 較為實用，可以用 `(_ for _ in ()).gi_code.__class__` 獲得。

剩下填入 code object argument 的部分就比較冗了，就只是照著填而已。

這邊直接寫個腳本完成上述的操作

```python
def generator(func):
    co = func.__code__
    return f'''
[
    func_class:=(lambda:None).__class__,
    code_class:=(_ for _ in ()).gi_code.__class__,
    func_class(
        code_class({co.co_argcount}, 0, {co.co_kwonlyargcount}, {co.co_nlocals},
                    {co.co_stacksize}, {co.co_flags}, {co.co_code}, {co.co_consts}, {co.co_names},
                    {co.co_varnames}, "filename.py", "meow_func", {co.co_firstlineno}, b""
        )
        , {{}}
    )
][-1]()'''.replace("    ", "").replace("\n", "")
```

至此，我們已經完成所有必要的前置作業，剩下就是 python sandbox 的老梗了：
1. 列出 `<class 'object'>` 的 subclasses
2. 找到好用的 gadget
3. 執行任意指令

這部分就去看 solution.py 吧



最後，或許有人會想到，你前面那個 `addaudithook` 沒提到欸，這到底是什麼：
```python
def hook(event, args):
    if not all([e not in ['subprocess', 'system', 'spawn'] for e in event.split(".")]):
        print("Bad system call (core dumped)")
        sys.exit()


sys.addaudithook(hook)
```

可以參考一下[官方文件](https://docs.python.org/3/library/audit_events.html)，是 Python 3.8 的新東西，不過在這題其實只是寫好玩的而已，主要功能只有防止你執行 `os.system` 之類的東西，但其實不太影響解題。
