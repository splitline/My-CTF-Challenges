# Cat Translator

- Category: Misc
- Static Score: 250 / 500
- Solves: 4 / 25

## Solution

### TL;DR
1. Find the hint hidden by `"\r"` and get the source code.
2. `re.search("[a-zA-Z0-9 ]+", input) and eval(input)`
3. Use feature PEP-3131 to bypass the limitation.

### Detailed Solution

基本上這題是一個沒什麼營養的題目，但抱歉R，tag 有 troll，就是要整你各位一下 >_^

nc 上去之後，一開始會直接 print 一句話：`Welcome to Cat Translator, you can only type 喵 or ニャーン here!`。但其實在印出這句話之前，他還有印出一句 hint，但由於 `\r`（carriage return）字元的影響而被覆蓋掉了：
```python
print("Hint: Type `原始碼` or `ソースコード` to get the source code.\rWelcome to Cat Translator, you can only type 喵 or ニャーン here!\n")
```

> 話說有幾個人直接通靈出要打「原始碼」這三個字，也是靈力蠻充足的 = =

拿到原始碼之後會看到一坨壓過的 code（以及出師表 XD），重點其實可以簡化成這樣：
```python
not __import__('re').search("[a-zA-Z0-9 ]+", code) and eval(code)
```

也就是說，輸入的內容只要不包含 alphanumeric 和空白，它就會去直接 eval 你的輸入了，乍看之下或許像要構造出類似 PyFuck(?) 的東西，但其實繞過的方法相當簡單：只要把所有英文的 identifiers 換成全行字元（大多數人似乎都是這麼做的）就行了！

問題來了，這到底是什麼奇怪 feature 呢？其實這被規範在 [PEP-3131](https://www.python.org/dev/peps/pep-3131/)（PEP 全文是 Python Enhancement Proposals，基本上各種 Python feature 都基於此設計的）。

簡單來說，它提到了所有 Python script 中的 Non-ASCII identifiers 在被直譯時，都會先經過一層 NFKC-normalization 的處理，因此那些全形英文字元都會被 normalize 回普通的英文字，並會維持原本的大小寫。而關於 NFKC 以及各種 normalization 的官方定義可以看這份 report：https://unicode.org/reports/tr15/；熟悉 web / web security 的人，或許會發現這個其實跟 SSRF bypass 經典招數之一：IDNA normalization 有點異曲同工之妙。

總之，在知道這個 feature 之後 payload 就能很簡單的設計了，不過只是換成全型字元實在有些無趣，這邊附個看起來比較豐富的版本 XD

```python
＿＿𝙞𝙢𝙥𝙤𝙧𝙩__(𝓲𝓷𝓹𝓾𝓽()).𝖘𝖞𝖘𝖙𝖊𝖒(𝕚𝕟𝕡𝕦𝕥())
```
