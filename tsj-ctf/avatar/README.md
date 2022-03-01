# Avatar

- Tags: `Web`
- Solves: 1 / 428
- Attachment: `release.zip`

## TL;DR

### Way to exploit

1. CRLF injection to SSRF redis; setting serialized session
2. Trigger RCE by using a POP chain in [FluentPDO](https://github.com/envms/fluentpdo)

### Key points

1. You can inject another Host header in `stream_context_create` to bypass [the protection of redis](https://github.com/redis/redis/commit/874804da0c014a7d704b3d285aa500098a931f50).
2. Find the long (?) POP chain.

## Description

This is a simple website that you can login / register your account and upload your avatar by either file or URL. And the SQL query operations is based on the FluentPDO library.

And the main vulnerabilities occur in `upload.php`.

### SSRF

In `update.php`, it does some check for URL uploading. Basically, it checks that url should start with `http://` or `https://`, then checks the ip address of the url (`gethostbyname($parsed_url['host'])`) is not local address by using `filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)`. 

If all of these checks are passed, it'll fetch the URL by `file_get_contents` and set the avatar.

But it's easy to bypass. Of course, you can use DNS rebinding to bypass the IP check, because there is a small delay between checking and fetching. But that's not stable. 

Actually `file_get_contents` (http stream in PHP, exactly) follows the redirection by default. So you just need to set your server redirecting to any URL you want, that's all.

### CRLF injection

The fetching part looks a little weird, it gets the file extension of the URL path, then urldecode it, then set to the `Accept` header:

```php
$image_type = pathinfo(urldecode($parsed_url['path']), PATHINFO_EXTENSION) ?? 'png';
$image = file_get_contents($url, false, stream_context_create([
    'http' => ['header' => [
        "Accept: image/$image_type",
        "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    ]]
]));
```

Actually there is a (intended) CRLF injection feature in `stream_context_create`. So you can use `http://host/a.b%0D%0Ameow` to inject CRLF.


### Control Redis

The first things you need to know is that PHP session is stored in serialized format, so once you can control the content of session, you got a deserialization vulnerbility.

In this challenge, you need to control redis to set arbitrary value for session. For example, you can use command `SET PHPREDIS_SESSION:<PHPSESSID> <VALUE>` to set the content of your session.

Seems we've got a CRLF injection, so that's all? Not really. Redis [implements a protection](https://github.com/redis/redis/commit/874804da0c014a7d704b3d285aa500098a931f50) against this kind of attack. Once redis receives `Host` or `POST`, it'll cut off the connection.

And the http packet sent by `file_get_contents` looks like this:
```
GET / HTTP/1.0
Host: example.com
Connection: close
Accept: image/<INJECTION_POINT>
User-Agent: Mozilla/5.0 ...
```

The injection point is after the `Host` header, so the connection will get closed. And the bypassing way is just to  inject our own `Host` header, then PHP will automatically replace the old one.

For example, if you post `url=http://host/a.b%0D%0ASET%20PHPREDIS_SESSION:48763%20NYAN%0D%0AHost:%20gg`, the `file_get_contents` should send:

```
GET / HTTP/1.0
Connection: close
Accept: image/b
SET PHPREDIS_SESSION:48763 NYAN
Host: gg
User-Agent: Mozilla/5.0 ...
```

In this way, you can send any command to redis now! 

> P.S. You might want to use SLAVEOF, MODULE LOAD or other known tricks to get RCE in the first place, but those commands are renamed in `redis.conf` so that won't work.

### POP Chain

Where can we trigger the POP chain? There is no `__destruct` or `__wakeup` in FluentPDO, which is a common entry point for POP chain. But that's not a problem, we can also use `__toString()` to trigger it. In `index.php` there is a code like this: `$user = $fluent->from('users')->where('username', $_SESSION['username'])->fetch()`, which will automatically convert `$_SESSION['username']` to string!


It's a little hard to explain the whole chain, so just read my exploit :D

See [gadgets.php](./exploit/gadgets.php), the following is the call stack to execute arbitrary command:

```
$key($table)
Envms\FluentPDO\Structure->key(system, ls)
Envms\FluentPDO\Structure->getPrimaryKey(ls)
Envms\FluentPDO\Queries\Common->createJoinStatement(LEFT JOIN, ls, a, a)
Envms\FluentPDO\Queries\Common->applyTableJoin(LEFT JOIN, Array (), ls, a:, a:, )
Envms\FluentPDO\Queries\Common->addJoinStatements(LEFT JOIN, a:)
Envms\FluentPDO\Queries\Common->createUndefinedJoins(a:b)
array_map(...)
Envms\FluentPDO\Queries\Common->buildQuery()
Envms\FluentPDO\Queries\Base->getQuery()
Envms\FluentPDO\Queries\Base->__toString()
```

### Exploit

1. Post `url` to set your session to that POP chain.
2. Get `index.php` to trigger the RCE.

See [exploit.py](./exploit/exploit.py).

Note that if your command contains `/` or `.`, your serialized data might not work because the `pathinfo` will break it. In this case, you can try things like `bash -c '\${PATH:0:1}readflag give me the flag'` or escape with [another serialization format](https://github.com/ambionics/phpggc#ascii-strings).


