# Genie

- Tags: `Web`, `Crypto`
- Solves: 1 / 428
- Attachment: `chall.tar.gz`

> I designed this challenge with [@maple3142](https://github.com/maple3142) together, and the challenge source code is written by him.

## TL;DR

This is kinda a 0-day challenge.

1. Upload [malicious serialized data](https://github.com/JuliaLang/julia/issues/32601) with filename from `"sessions/\x01"` to `"sessions/\xFF"`. (using the path traversal bug)
2. Forge your session to make your session has only one character, so you can trigger the deserialization easily.

## Description

> This is a file hosting website made with [Genie.jl](https://github.com/GenieFramework/Genie.jl). You can upload any file to the server and view it.

### Path traversal

Obviously, there is a path traversal vulnerability when you upload a file:
```julia
route("/upload", method = POST) do
  if infilespayload(:file)
    f = filespayload(:file)
    p = joinpath(upload_dir, f.name)
```
If the file name is `../xxx`, then the file will be uploaded to the parent folder (`/app`) instead of the `upload` directory.

But where can we write to exploit this vulnerability?

### Deserialization?

First thing you need to know is that the deserialization operation in Julia is dangerous, you can refer to [this issue](https://github.com/JuliaLang/julia/issues/32601) for the PoC.

Then you should notice that Genie.jl uses serialization to store the session data in file (in `sessions/<filename>` directory) by default: https://github.com/GenieFramework/Genie.jl/blob/v4.14.0/src/Sessions.jl#L265

So once we can know the exact filename of our current session, then we can craft a serialized data and write it to the session directory to get RCE.

### Cryptography Bug

Now let's take a look at how it maps session id in our cookie to the filename.

Basically, the session id is actually an encrypted string of the filename, you can see that Genie.jl uses [encrypted cookie by default](https://github.com/GenieFramework/Genie.jl/blob/v4.14.0/src/Cookies.jl#L74-L81), and the encryption way is [AES in CBC mode](https://github.com/GenieFramework/Genie.jl/blob/master/src/Encryption.jl#L16-L21).

Wait a minute, **CBC**? Seems like we can use padding oracle to attack it? Well, not really, because [it's IV is fixed](https://github.com/JuliaCrypto/Nettle.jl/blob/master/src/cipher.jl#L78-L83) (generated from `Genie.secret_token` exactly) and we don't have any way to change it (and the unpadding function never throws padding error by the way).

How about the **bit flipping attack**? We can't control the IV, which means we can never manipulate the first block of plaintext -- but that's enough.

Actually we've know the plaintext of the last block. Because PKCS#5 padding is used, and [the filename is always 64 bytes long](https://github.com/GenieFramework/Genie.jl/blob/v4.14.0/src/Sessions.jl#L46-L51), which means the last block is always filled with padding `bytes([16])*16`.

The blocks before unpadding look like this:

```
      block#1           block#2           block#3           block#4             block#5
+-----------------+-----------------+-----------------+-----------------+---------------------+
|  Filename[:16]  | Filename[16:32] | Filename[32:48] | Filename[48:64] | Padding ("\x10"*16) |
+-----------------+-----------------+-----------------+-----------------+---------------------+
```

We know in the decryption of CBC mode, the last block (block#5) is xored with the ciphertext of previous block (block#4). Since we've know the plaintext of block#5, we can forge arbitrary data of it, Just simply do the following:

```
Ciphertext(block#4) = ("\x10" * 16) XOR Ciphertext(block#4) XOR Target(block#5)
```

We can manipulate the last block of the decrypted plaintext now, this will break the plaintext of block#4 obviously, but it won't affect our exploitation.

Actually the unpadding function [just takes the last byte of the padding as the padding length](https://github.com/JuliaCrypto/Nettle.jl/blob/master/src/cipher.jl#L90-L93), it doesn't check it at all, so we can easily make the padding length be `len(plaintext) - 1`, then we can get a plaintext with only one byte!

To sum up, we need to craft a ciphertext like this:
```
ForgedCiphertext = (("\x10" * 16) XOR Ciphertext(block#4) XOR ("\x1f" * 16)) + CipherText(block#5)

p.s. "\x1f" means (32 - 1), which is the padding length -- we only have two blocks now.
```
then we can get a plaintext with only one byte.

> We can't and don't need to really know what the "one byte" is.

### Trigger the Deserialization

We have a path traversal bug to upload a file to any path, and we can craft the filename of our session to only one byte, let's talk about how to exploit it.

You just need to simply upload 254 malicious serialized data with the filename from `"../sessions/\x01"` to `"../sessions/\xFF"` (excluding `"."` and `"/"`), then forged a one byte session id to trigger the deserialization.

As we mentioned in the previous section, we don't need to really know what the "one byte" is, because we've uploaded a lot of one byte filename session files, there is a high chance to match one of them.

Note that we need to trigger the deserialization twice, because the first time is just overwriting the `Serialization.deserialize(s::Serializer, t::Type{...})` method, and the second time really triggers the RCE.

For the full exploit please check our [exploit script](exploit/exploit.py).

## Postscript

I've opened an issue about this bug, see [Genie.jl#493](https://github.com/GenieFramework/Genie.jl/issues/493).

