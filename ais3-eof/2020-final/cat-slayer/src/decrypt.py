import random
import time
import datetime
import os

if __name__ == '__main__':
    seed = int(os.stat('cat_slayer.data.meow').st_mtime) - 10
    enc_data = open("cat_slayer.data.meow", 'rb').read()
    while True:
        random.seed(seed)
        n = 8
        dec = ''
        for c in enc_data:
            key = random.randint(22, 222) + (n * 3 - 5) % 22
            dec += chr(c ^ key)
            n += 3
        if dec.startswith("___GAME_CAT"):
            print(seed)
            print(dec)
            break
        seed += 1

