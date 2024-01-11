from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import secrets
import os

FLAG = os.getenv("FLAG")

class AESToken:
    def __init__(self, secret):
        self.iv = secret[:16]
        self.key = secret[16:]

    def decrypt(self, data, **kwargs):
        cipher = AES.new(self.key, **kwargs)
        data = cipher.decrypt(data)
        return unpad(data, AES.block_size)

    def encrypt(self, data, **kwargs):
        cipher = AES.new(self.key, **kwargs)
        data = pad(data, AES.block_size)
        return cipher.encrypt(data)

    def load(self, token):
        data = bytes.fromhex(token)
        data = self.decrypt(data=data, mode=AES.MODE_OFB, iv=self.iv)
        data = self.decrypt(data=data, mode=AES.MODE_ECB)
        return json.loads(data.decode())

    def dump(self, data):
        data = json.dumps(data).encode()
        data = self.encrypt(data=data, mode=AES.MODE_ECB)
        data = self.encrypt(data=data, mode=AES.MODE_OFB, iv=self.iv)
        return data


if __name__ == "__main__":
    secret = secrets.token_bytes(32)
    token_manager = AESToken(secret)
    while True:
        print('=== Menu ===')
        print('1. Login')
        print('2. Register')
        print('3. Exit')
        choice = input('Enter your choice: ')
        try:
            match choice:
                case '1':
                    token = input('Enter your token: ')
                    data = token_manager.load(token)
                    if data['user_id'] == 'admin' and data['admin'] == True:
                        print(f'Wow, you are admin! Here is your flag: {FLAG}')
                    else:
                        print(f'Hello, {data["user_id"]}!')
                case '2':
                    name = input("Welcome! What's your username? ")
                    if name == "admin":
                        print("No, you're not.")
                        exit()
                    data = {"user_id": name, "admin": False}
                    token = token_manager.dump(data)
                    print(f"Hello, {name}!")
                    print("Here is your token:", token.hex())
                case '3':
                    exit()
                case _:
                    print("Invalid choice")
        except Exception as e:
            print("Error:", e)
