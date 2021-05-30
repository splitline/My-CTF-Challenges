#!/usr/local/bin/python
import random
import os
import pickle
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

sys.stdin.reconfigure(encoding='ISO-8859-1')

key = os.getenv('KEY', 'test_keymeowmeow').encode()
cipher = AES.new(key, AES.MODE_ECB)
BLOCK_SIZE = 16


def enter2continue():
    input("=== PRESS ENTER TO CONTINUE ===")


class CatSlayer:
    def __init__(self, hp, attk, defs, money):
        self.username = "<guest>"
        self.hp = hp
        self.attk = attk
        self.defs = defs
        self.money = money

    def set_name(self, name):
        self.username = name


player = CatSlayer(1000, 10, 0, 0)


def fight():
    rounds = 0
    print('\033c')
    level = input("Level [1,2,3,...]: ")
    if not level.isdigit() or int(level) == 0:
        return
    cat_power = pow(10, int(level) - 1)
    demon_names = ["Buné", "Samigina", "Ronové", "Vassago", "Purson", "Glasya-Labolas", "Caim", "Gremory", "Vapula", "Asmoday", "Gäap", "Furcas", "Bifrons", "Valac", "Flauros", "Alloces", "Viné", "Andromalius", "Aim", "Phenex", "Agares", "Malphas", "Amdusias", "Halphas", "Dantalion", "Astaroth", "Marax", "Focalor", "Andras", "Botis", "Foras", "Shax", "Sabnock", "Furfur",
                   "Amy", "Marbas", "Ose", "Ipos", "Orias", "Amon", "Zepar", "Kimaris", "Leraje", "Bathin", "Forneus", "Buer", "Murmur", "Belial", "Haagenti", "Vual", "Eligos", "Naberius", "Vepar", "Beleth", "Balam", "Paimon", "Sallos", "Orobas", "Seere", "Barbatos", "Bael", "Valefor", "Räum", "Gusion", "Crocell", "Sitri", "Berith", "Stolas", "Andrealphus", "Zagan", "Decarabia"]
    while True:
        rounds += 1
        cat_name = random.choice(demon_names)
        cat_hp = random.randint(10, 50) * cat_power
        print('+' + "-"*32 + '+')
        print("|" + f"[Round {rounds}]".ljust(28, ' ').rjust(32, ' ') + "|")
        print("|" + f"Monster: Cat {cat_name}".ljust(28, ' ').rjust(32, ' ') + "|")
        print("|" + f"HP: {cat_hp}".ljust(28, ' ').rjust(32, ' ') + "|")
        print('+' + "-"*32 + '+')

        print("\n⚔ BATTLE START ⚔\n")
        while True:
            cat_attk = random.randint(5, 30) * cat_power
            cat_defs = random.randint(1, 5) * cat_power

            damage = max(cat_attk - player.defs, int(level))
            player.hp -= damage
            print(f"Cat {cat_name} attacks you.")
            print(f"Caused {damage} pts of damage. Your HP = {player.hp}.")
            if player.hp <= 0:
                print("You died \|/.")
                exit()

            cat_damage = max(player.attk - cat_defs, 1)
            cat_hp -= cat_damage
            print(f"You attacks Cat {cat_name}.")
            print(f"Caused {cat_damage} pts of damage. Cat's HP = {cat_hp}.")
            if cat_hp <= 0:
                print(f"Cat {cat_name} died \|/.")
                player.money += cat_power * cat_power
                print(f"Drop some coins! [${cat_power * cat_power}]")
                break
        while True:
            cont = input("Next Cat (y/n): ")
            if cont == 'y':
                break
            elif cont == 'n':
                return


def shop():
    while True:
        print(f'''\033c
[Shop]
========
Your Money = {player.money}
========
(H)P + 5 / $1
(A)ttack + 10 / $5
(D)efense + 10 / $5
(F)lag / $2147483647
(B)et / $100
(Q)uit
    ''')
        choose = input("Choose: ")
        if choose == 'H' and player.money >= 1:
            player.money -= 1
            player.hp += 5
        elif choose == 'A' and player.money >= 5:
            player.money -= 5
            player.attk += 10
        elif choose == 'D' and player.money >= 5:
            player.money -= 5
            player.defs += 10
        elif choose == 'B' and player.money >= 100:
            player.money -= 100
            if random.randint(0, 1000) == 999:
                player.money = 0x7fffffff
            else:
                player.money = -0x7fffffff
        elif choose == 'F' and player.money >= 0x7fffffff:
            player.money -= 0x7fffffff
            # flag = open(os.getenv("flag_path"), 'read').get_content()
            # print("[FLAG]", flag)
            input("I forget how to get a file's content in python, sorry :(")
        elif choose == 'Q':
            return


def menu():
    print('''\033c
[Menu]
========
(S)tatus
(F)ight
(B)uy
(L)oad Game
Sa(V)e Game
(Q)uit
        ''')
    return input("Choose: ")


def game():
    global player
    print("""\033c
   ______      __     _____ __
  / ____/___ _/ /_   / ___// /___ ___  _____  _____
 / /   / __ `/ __/   \__ \/ / __ `/ / / / _ \/ ___/
/ /___/ /_/ / /_    ___/ / / /_/ / /_/ /  __/ /
\____/\__,_/\__/   /____/_/\__,_/\__, /\___/_/
                                /____/

☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ [CLOUD EDITION] ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ ☁️ 

            🐈 <- THEY ARE EVIL QwQ
""")

    player.set_name(input("Name: "))
    while True:
        choose = menu()
        if choose == 'S':
            print(f'''\033c
[Status]
========
Name: {player.username}
HP: {player.hp}
Attack: {player.attk}
Defense: {player.defs}
Money: {player.money}
                '''.strip())
            enter2continue()
        elif choose == 'F':
            fight()
        elif choose == 'B':
            shop()
        elif choose == 'L':
            enc_data = input("Saved Data: ")
            if enc_data:
                try:
                    game_data = unpad(cipher.decrypt(bytes.fromhex(enc_data)), BLOCK_SIZE)
                    player = pickle.loads(game_data)
                except:
                    print("[x] Invalid data.")
            enter2continue()
        elif choose == 'V':
            game_data = pickle.dumps(player)
            print("Saved Data:", cipher.encrypt(pad(game_data, BLOCK_SIZE)).hex())
            enter2continue()
        elif choose == 'Q':
            break


if __name__ == '__main__':
    game()
