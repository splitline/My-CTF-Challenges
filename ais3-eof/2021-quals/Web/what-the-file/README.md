# What the File

- Category: Web
- Solves: 15 / 95 (scores >= 1), 55 (scores > 1)

## Solution

1. Control `file` command's output. (e.g. use Shebang `#! meow`)
2. Solution 1: Use `convert.base64-decode`
   1. 利用 php 中 base64 會忽略非 base64 字元的特性。
   2. 寫入 base64 encode 過的 webshell 到 Shebang（並控制 offset 使其能正常 decode）
   3. 用 `php://filter/write=convert.base64-decode/resource=file` 寫入檔案
3. Solution 2: Use `convert.iconv`
   1. 利用 utf-7 會把 `<`, `>` 分別轉為 `+ADw`, `+AD4-` 的特性。
   2. 寫入 utf-7 encode 的 webshell 到 Shebang
   3. 用 `php://filter/write=convert.iconv.utf-7.utf-8/resource=file` 寫入檔案
4. 利用 `shell.php/.` 作為檔名，使 `pathinfo` 抓不到副檔名，但 `file_put_contents` 能正常寫入檔案
5. Get Shell!