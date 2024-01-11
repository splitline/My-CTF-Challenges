# My CTF Challenges

#### HITCON CTF 2023

[write-up](https://blog.splitline.tw/hitcon-ctf-2023/)

| Challenge | Category  | Description                                                  |
| --------- | --------- | ------------------------------------------------------------ |
| Sharer    | web       | XSS and CSRF with [Signed Exchange](https://web.dev/articles/signed-exchanges) (SXG) feature. |
| AMF       | web, misc | Find an RCE gadget in [Py3AMF](https://github.com/StdCarrot/Py3AMF) |

#### HITCON CTF 2022

[write-up](https://blog.splitline.tw/hitcon-ctf-2022/)

| Name                                               | Category | Description                                                  |
| -------------------------------------------------- | -------- | ------------------------------------------------------------ |
| [🎲 RCE](hitcon-ctf/2022/web/rce)                   | web      | Warmup Challenge                                             |
| [💣 Self Destruct Message](hitcon-ctf/2022/web/sdm) | web      | XSS                                                          |
| [🎧 S0undCl0ud](hitcon-ctf/2022/web/S0undCl0ud)     | web      | Python generator, [mimetypes](https://docs.python.org/3/library/mimetypes.html) library |
| [📃 web2pdf](hitcon-ctf/2022/web/web2pdf)           | web      | [mpdf](https://github.com/mpdf/mpdf.git) 0-day               |
| [V O I D](hitcon-ctf/2022/misc/void)               | misc     | Using OOB bytecodes to escape PyJail                         |
| [🥒 Picklection](hitcon-ctf/2022/web/picklection)   | misc     | Pickle Jail                                                  |

**Balsn CTF **

**2023**

| Name  | Category | Description                |
| ----- | -------- | -------------------------- |
| Memes | web      | `imagepng` + FTP PASV SSRF |

#### TSJ CTF 2022

| Name                                                | Category       | Description                                                  |
| --------------------------------------------------- | -------------- | ------------------------------------------------------------ |
| [Genie](./tsj-ctf/genie/)                           | Web, Crypto    | [Genie.jl](https://github.com/GenieFramework/Genie.jl) 0-day, Julia deserialization, Bit flipping |
| [Avatar](./tsj-ctf/avatar/)                         | Web            | Redis SSRF, CRLF injection, POP chain                        |
| [Welcome to TSJ CTF](./tsj-ctf/welcome-to-tsj-ctf/) | Web, Misc, CSC | .DS_Store, Guessing                                          |

#### AIS3 EOF CTF

**2023 Final**

| Name | Category | Description                     |
| ---- | -------- | ------------------------------- |
| WoW  | KoH      | Web-based 2D battle royale game |

**2023 Quals**

| Name              | Category | Description                         |
| ----------------- | -------- | ----------------------------------- |
| Monsieur de Paris | Misc     | Python multiprocessing RPC (pickle) |

**2022 Final**

| Name         | Category | Description                                                |
| ------------ | -------- | ---------------------------------------------------------- |
| npy viewer   | Web      | 0-day in [jpickle](https://github.com/jlaine/node-jpickle) |
| Imgura Final | Web, A&D | PHP A&D challenge                                          |

**2022 Quals**

| Name                                                         | Category | Description                                                  |
| ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| [SSRF challenge or not?](ais3-eof/2021-quals/Web/ssrf-or-not/) | Web      | `file://`, signed pickle cookie, [Bottle](https://bottlepy.org/docs/dev/) |
| [Happy Metaverse Year](ais3-eof/2021-quals/Web/happy-metaverse-year/) | Web      | Union+blind based SQLi                                       |
| [babyphp](ais3-eof/2021-quals/Web/babyphp/)                  | Web      | .htaccess, `php://filters` chain                             |
| [GistMD](ais3-eof/2021-quals/Web/gistmd/)                    | Web      | JSONP, DOM clobbering                                        |
| [Imgura album](ais3-eof/2021-quals/Web/imgura-album/)        | Web      | Path traversal, PHP session , POP chain in [Flight](https://github.com/flightphp/core) framework |
| [PM](ais3-eof/2021-quals/Web/pm/)                            | Web      | FPM SSRF                                                     |
| [LeetCall](ais3-eof/2021-quals/Misc/leetcall/)               | Misc     | Write Python with only Call, Name and Constant nodes         |
| [babyheap](ais3-eof/2021-quals/Misc/babyheap/)               | Misc     | argument injection (`wget`, `zip`)                           |

**2021 Quals**

| Name                                                    | Category | Keywords                                                     |
| ------------------------------------------------------- | -------- | ------------------------------------------------------------ |
| [WTF](ais3-eof/2020-quals/Web/what-the-file)            | Web      | php wrapper, `file` command                                  |
| [CYBERPUNK 1977](ais3-eof/2020-quals/Web/CYBERPUNK1977) | Web      | SQL injection, quine, python format string                   |
| [CTF Note](ais3-eof/2020-quals/Web/ctf-note)            | Web      | prototype pollution (gadget in [markdown-js](https://github.com/evilstreak/markdown-js)), DOM clobbering, RPO |
| [3DUSH3LL](ais3-eof/2020-quals/Misc/3DUSH3LL)           | Misc     | Pyjail                                                       |

#### 2021 Final

> All of my challenges in this CTF are related to Python XD

| Name                                                 | Category | Keywords              |
| ---------------------------------------------------- | -------- | --------------------- |
| [Pikora](ais3-eof/2020-final/pikora)                 | Misc     | PPC but use pickle    |
| [Cat Translator](ais3-eof/2020-final/cat-translator) | Misc     | Troll, PyJail         |
| [Cat Slayer](ais3-eof/2020-final/cat-slayer)         | Reverse  | Python bytecode (pvc) |

#### AIS3 Pre-Exam

**2022**

| Name          | Category | Description                               |
| ------------- | -------- | ----------------------------------------- |
| Double AES    | Crypto   | OFB(ECB(data)), cut & paste, JSON         |
| ASTJail       | Misc     | PyJail                                    |
| TariTari      | Web      | Warmup, path traversal, command injection |
| Best Login UI | Web      | NoSQL injection                           |
| Emoji DB      | Web      | SQL Server SQL injection                  |
| Gallery       | Web      | Upload SVG to XSS, `default-src 'self'`   |

**2021**

   [Web](ais3-pre-exam/2021/Web/) | [Reverse](ais3-pre-exam/2021/Reverse/) | [Misc](ais3-pre-exam/2021/Misc/)

| Name                         | Category | Keywords                              |
| ---------------------------- | -------- | ------------------------------------- |
| 🐰 Peekora 🥒                  | Reverse  | Pickle Bytecode                       |
| ⲩⲉⲧ ⲁⲛⲟⲧⲏⲉꞅ 𝓵ⲟ𝓰ⲓⲛ ⲣⲁ𝓰ⲉ       | Web      | JSON injection                        |
| 【5/22 重要公告】            | Web      | LFI, SQL injection, Command injection |
| XSS Me                       | Web      | XSS with length limit                 |
| Cat Slayerᴵⁿᵛᵉʳˢᵉ            | Web      | Java Deserialization, Reflection      |
| Cat Slayer \| Cloud Edition  | Misc     | Pickle, ECB Cut&Paste                 |
| Cat Slayer \| Online Edition | Misc     | Game, Python Sandbox                  |

