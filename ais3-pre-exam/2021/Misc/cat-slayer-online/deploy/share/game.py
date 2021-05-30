#!/usr/local/bin/python
import random
import time
import math
import subprocess
import os
import re
import sqlite3
import secrets
import signal

EASY_MODE = False

conn = sqlite3.connect("./player.db")
conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))


class Player():
    def __init__(self, player_name='', token='', hp=100, attack=15, defense=0, money=0,
                 killer=False, kill_num=0, last_kill=0, killed=False, max_level=0, unlocked=[],
                 rebirthed=False,
                 load=False):
        if load:
            res = conn.cursor().execute("SELECT * FROM Player where player_name=?", (player_name,)).fetchone()
            res.pop('id')
            unlocked = res.pop('unlocked')
            self.unlocked = list(map(int, unlocked.split(","))) if unlocked.strip() else []
            for attr, val in res.items():
                self.__setattr__(attr, val)
            return
        self.player_name = player_name
        self.token = token
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.money = money
        self.killer = killer
        self.kill_num = kill_num
        self.last_kill = last_kill
        self.killed = killed
        self.max_level = max_level
        self.unlocked = unlocked
        self.rebirthed = rebirthed

    def get_max_spell(self):
        return self.max_level * int(2/math.log10(max(2, len(self.unlocked)-10))*6)

    def rebirth(self):
        self.hp = 100
        self.attack = 15
        self.defense = 0
        self.money = 0
        self.killer = False
        self.kill_num = 0
        self.last_kill = 0
        self.killed = False
        self.max_level = 0
        self.unlocked = []

        self.rebirthed = True

    def save(self, new_player=False, died=False, kill=False, is_killer=False):
        _dict = self.__dict__
        __unlocked = _dict['unlocked'].copy()
        _dict['unlocked'] = ','.join(map(str, _dict['unlocked']))
        cursor = conn.cursor()
        if new_player:
            _dict['token'] = secrets.token_hex(16)
            cursor.execute(
                f'INSERT INTO Player({",".join(_dict.keys())}) VALUES ({",".join("?"*len(_dict)) })',
                tuple(_dict.values()))
        else:
            is_killed = Player.get_player(self.player_name)['killed']
            if is_killed:
                print("💀 Oops, you just got murdered by another player Q_Q")
                exit()
            if died:
                _dict['money'] = 0
                _dict['hp'] = 100
                _dict['attack'] = max(int(self.attack*0.5), 15)
                _dict['defense'] = int(self.defense * 0.5)
                _dict['max_level'] = max(int(self.max_level - 2), 0)
            if kill:
                _dict['killer'] = is_killer or _dict['killer']
                _dict['kill_num'] += 1
                _dict['last_kill'] = int(time.time())
            update_stmt = ', '.join([f"{key} = ?" for key in _dict.keys()])
            cursor.execute(
                f'UPDATE Player SET {update_stmt} WHERE player_name=?',
                tuple(_dict.values()) + (self.player_name,))

        conn.commit()
        _dict['unlocked'] = __unlocked

    @staticmethod
    def get_player(player_name):
        res = conn.cursor().execute("SELECT * FROM Player where player_name=?", (player_name,)).fetchone()
        return res


class Cat:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.power = pow(25, level - 1)
        self.hp = round(random.uniform(10, 50) * self.power)

    def get_attack(self):
        return int(random.uniform(1, 5) * self.power)

    def get_defense(self):
        return int(random.uniform(1, 5) * max(self.power/2, 1))


player: Player = None


def fight():
    global player

    rounds = 0
    print('\033c')
    cat_level = input("Level [1,2,3,...]: ")
    if not cat_level.isdigit() or int(cat_level) == 0:
        return
    cat_level = int(cat_level)
    demon_names = ["Buné", "Samigina", "Ronové", "Vassago", "Purson", "Glasya-Labolas", "Caim", "Gremory", "Vapula", "Asmoday", "Gäap", "Furcas", "Bifrons", "Valac", "Flauros", "Alloces", "Viné", "Andromalius", "Aim", "Phenex", "Agares", "Malphas", "Amdusias", "Halphas", "Dantalion", "Astaroth", "Marax", "Focalor", "Andras", "Botis", "Foras", "Shax", "Sabnock", "Furfur",
                   "Amy", "Marbas", "Ose", "Ipos", "Orias", "Amon", "Zepar", "Kimaris", "Leraje", "Bathin", "Forneus", "Buer", "Murmur", "Belial", "Haagenti", "Vual", "Eligos", "Naberius", "Vepar", "Beleth", "Balam", "Paimon", "Sallos", "Orobas", "Seere", "Barbatos", "Bael", "Valefor", "Räum", "Gusion", "Crocell", "Sitri", "Berith", "Stolas", "Andrealphus", "Zagan", "Decarabia"]
    while True:
        rounds += 1
        cat = Cat(random.choice(demon_names), cat_level)

        print('+' + "-"*32 + '+')
        print("|" + f"[Round {rounds}]".ljust(28, ' ').rjust(32, ' ') + "|")
        print("|" + f"Monster: Cat {cat.name}".ljust(28, ' ').rjust(32, ' ') + "|")
        print("|" + f"HP: {cat.hp}".ljust(28, ' ').rjust(32, ' ') + "|")
        print('+' + "-"*32 + '+')

        _round = 0
        print("\n⚔ BATTLE START ⚔\n")
        while True:
            if _round >= 20:
                print("Fight for 20 rounds zzzzzzz... You're totally tired (¦3[▓▓]")
                print("You lose _(:3」∠)_")
                player.save(died=True)
                exit()
            damage = max(cat.get_attack() - player.defense, cat_level)
            player.hp -= damage
            print(f"Cat {cat.name} attacks you.")
            print(f"Caused {damage} pts of damage. Your HP = {player.hp}.")
            if player.hp <= 0:
                print("You died \|/.")
                player.save(died=True)
                exit()

            cat_damage = max(player.attack - cat.get_defense(), 1)
            cat.hp -= cat_damage
            print(f"You attack Cat {cat.name}.")
            print(f"Caused {cat_damage} pts of damage. Cat's HP = {cat.hp}.")
            if cat.hp <= 0:
                print(f"Cat {cat.name} died \|/.")
                drop_money = cat.power * random.randint(1, 3)
                if EASY_MODE:
                    drop_money *= 100
                player.money += drop_money
                print(f"Drop some coins! [${drop_money}]")
                player.max_level = max(cat_level, player.max_level)
                break
            _round += 1
        while True:
            cont = input("Next Cat (y/n): ").lower()
            if cont == 'y':
                break
            elif cont == 'n':
                return


def list_users():
    def print_table(players):
        print()
        print(f"{'Player Name':>16} {'Max Level':>12} {'HP':>16} {'Attack':>16} {'Defense':>16} {'Money':>16}")
        print("-"*100)
        for p in players:
            fmt = "{player_name:>16} {max_level:>12} {hp:>16} {attack:>16} {defense:>16} {money:>16}"
            if p['kill_num']:
                fmt = fmt + '  🔪 {kill_num}'
            if p['killer']:
                fmt = '\033[91m' + fmt + ' \033[0m'
            print(fmt.format(**p))
    while True:
        choice = input("List (A)ll / (S)ame Level / (Q)uit: ").upper()
        if choice in ["A", "S", "Q"]:
            break

    cursor = conn.cursor()
    if choice == "A":
        all_players = cursor.execute(
            "SELECT * FROM Player where killed=0 and max_level!=0 ORDER BY max_level DESC LIMIT 100"
        ).fetchall()
        print_table(all_players)
        input("=== PRESS ENTER TO CONTINUE ===")
    if choice == "S":
        if player.max_level == 0:
            input("At least lv.1 to list players.")
            return
        all_players = cursor.execute(
            "SELECT * FROM Player where killed=0 and max_level=? LIMIT 100",
            (player.max_level,)
        ).fetchall()
        print_table(all_players)
        print("(K)ill / (Q)uit")
        option = input("Option: ").upper()
        if option != "K":
            return

        if player.max_level < 3:
            input("You're too young, only max level >= 3 can kill others...")
            return
        if (time_diff := int(time.time()) - player.last_kill) < 60*15:
            input(f"Calm down killer, {15-int(time_diff/60)} mins left for next kill :)")
            return
        target_player_name = input("Target player name: ")
        if target_player_name == player.player_name:
            input("lol, you can't suicide here. If you insist just go fight with some lv.100 cats🐱 :D")
            return
        target_player = Player.get_player(target_player_name)
        if target_player == None:
            input("[Wut?] No such player.")
            return

        if target_player['max_level'] < 3 or target_player['max_level'] < player.max_level - 1:
            input("Don't bully kids plz :(")
            return

        notice_you, first = random.randint(0, 2), True
        while True:
            if notice_you or not first:
                if notice_you and first:
                    print(f"Oops, {target_player_name} notice you.")
                print(f"Player {target_player_name} attacks you!")
                damage = max(target_player['attack'] - player.defense, player.max_level)
                player.hp -= damage
                print(f"Caused {damage} pts of damage. Your HP = {player.hp}")
                if player.hp <= 0:
                    print("You died \|/.")
                    player.save(died=True)
                    exit()

            first = False
            damage = max(player.attack - target_player['defense'], player.max_level)
            target_player['hp'] -= damage
            print(f"You attack {target_player_name}!")
            print(f"Caused {damage} pts of damage, "
                  f"{target_player_name}'s HP = {target_player['hp']}")
            if target_player['hp'] < 0:
                player.attack += target_player['attack']
                player.defense += target_player['defense']
                player.money += target_player['money']
                conn.execute('UPDATE Player SET killed=1 WHERE player_name=?',
                             (target_player_name, ))
                conn.commit()
                player.save(kill=True, is_killer=target_player['killer'] != True)

                print(f"You killed {target_player_name}!")
                print(("Attack + {attack}\n"
                       "Defense + {defense}\n"
                       "Money + {money}\n").format(**target_player))
                input("=== PRESS ENTER TO CONTINUE ===")
                return


def shop():
    global player
    while True:
        print(f'''\033c
[Shop]
========
Your Money = {player.money}
========
(H)P + 3 / $1
(A)ttack + 10 / $10
(D)efense + 2 / $10
(Q)uit
    ''')
        choose = input("Choose: ").upper()
        try:
            if choose in ["H", "A", "D"]:
                n_unit = int(input("How many units you want? "))
        except:
            continue
        if choose == 'H' and player.money >= n_unit:
            player.money -= n_unit
            player.hp += n_unit*3
        elif choose == 'A' and player.money >= n_unit*10:
            player.money -= n_unit*10
            player.attack += n_unit*10
        elif choose == 'D' and player.money >= n_unit*10:
            player.money -= n_unit*10
            player.defense += n_unit*2
        elif choose == 'Q':
            return


def church():
    import string
    print("""\033c[Church]\nDefault Curses (blacklist): /[a-z0-9()'".]/\n==========""")
    blacklist = list(string.ascii_lowercase+string.digits+"()'\".")
    current_price = (lambda x: int(22*x*2**(x+2)+22*x+22))(len(player.unlocked))

    print("--- Normal Curses ---")
    for i, curse in enumerate(blacklist[:-3]):
        print(f"{i}) {curse}", "/ [lifted]" if i in player.unlocked else "")

    print("--- Rebirthed Player Only ---")
    print("> Will be lifted automatically after one player rebirthed.")
    for curse in blacklist[-3:]:
        print(f"#) {curse}", "/ [lifted]" if player.rebirthed else "")

    print("---")
    print(f"Lifted Curses: {len(player.unlocked)}")
    print(f'Your Money: ${player.money}')
    print(f"Current Price: ${current_price}")
    print("---")
    option = input("Choose a curse id to lift / (Q)uit\nOption: ")
    if option == "Q" or not option.isdigit():
        return
    option = int(option)
    if option < len(blacklist) - 3:
        if option in player.unlocked:
            input(f"[Error] Curse `{blacklist[option]}` have already lifted!")
            return
        if player.money < current_price:
            input("[Error] You don't have enough money")
            return
        player.money -= current_price
        player.unlocked.append(option)
        print(f"`{blacklist[option]}` lifted!")
        input("Success!")
    else:
        input("No such curse...")


def menu():
    print('''\033c
[Menu]
All your record will be saved when you back to here.
========
(S)tatus
(L)ist Players
(F)ight
(B)uy
(M)agic: Cast Magic Spell 🔯 
(C)hurch: Lift Curses 🔯
(R)ebirth 
(Q)uit
        ''')
    return input("Choose: ").upper()


def game():
    global player
    print("""\033c
   ______      __     _____ __                     
  / ____/___ _/ /_   / ___// /___ ___  _____  _____
 / /   / __ `/ __/   \__ \/ / __ `/ / / / _ \/ ___/
/ /___/ /_/ / /_    ___/ / / /_/ / /_/ /  __/ /    
\____/\__,_/\__/   /____/_/\__,_/\__, /\___/_/     
                                /____/             
            🐈 <- THEY ARE EVIL Q_Q
""")

    is_new = input("New Player? (y/n) ").lower() == 'y'
    if is_new:
        while True:
            player_name = input("Choose your player name: ")
            if not re.match(r"[a-z0-9_ ]", player_name, re.IGNORECASE) or len(player_name) > 16:
                print("Invalid name.")
                continue
            if Player.get_player(player_name) != None:
                print("Player exists.")
                continue
            player = Player(player_name)
            player.save(new_player=True)

            print("Register success!")
            input(f"Please record & save this token for login: {player.token}")
            input("=== PRESS ENTER TO CONTINUE ===")
            break
    else:
        player_name = input("Player Name: ")
        login_token = input("Token: ")
        if not re.match(r"[a-z0-9_ ]", player_name, re.IGNORECASE) or len(player_name) > 16:
            print("Invalid name.")
            return
        _player = Player.get_player(player_name)
        if _player == None:
            print("No such player.")
            return
        if _player['killed'] == True:
            print("You've been killed by other player, all your record have been locked Q_Q")
            return
        if _player['token'] != login_token:
            print("Token doesn't match.")
            return
        player = Player(player_name, load=True)
        input("=== PRESS ENTER TO CONTINUE ===")

    while True:
        choose = menu()
        if choose == 'S':
            print(f'''\033c
[Status]
========
Token: {player.token}
-
Name: {player.player_name}
HP: {player.hp}
Attack: {player.attack}
Defense: {player.defense}
Money: {player.money}
Max Level: {player.max_level}
-
Max spell length: {player.get_max_spell()} characters.
Lifted {len(player.unlocked)} curses.
Killed {player.kill_num} players.
Rebirthed? {["No","Yes"][player.rebirthed]}
                '''.strip())
            input("=== PRESS ENTER TO CONTINUE ===")
        elif choose == 'F':
            fight()
        elif choose == 'B':
            shop()
        elif choose == 'L':
            list_users()
        elif choose == 'C':
            church()
        elif choose == "R":
            ans = input("All your record will be reset, are you sure? (y/n)")
            if ans != 'y':
                continue
            if player.max_level >= 10:
                player.rebirth()
                input("REBIRTHED!")
            else:
                input("You can rebirth only when you win a lv.10 cat...")

        elif choose == 'M':
            max_spell_len = player.get_max_spell()
            print("Max spell length:", max_spell_len)
            spell = input("Your magic spell 🔯: ")
            print("🪄 🪄 🪄")
            try:
                subprocess.run(['python', 'sandbox.py',
                                spell,
                                ",".join(map(str, player.unlocked)),
                                str(max_spell_len),
                                str(int(player.rebirthed))
                                ], timeout=10, shell=False)
            except subprocess.TimeoutExpired:
                print("Timeout owO")
            input("(ﾉ>ω<)ﾉ :｡･:*:･ﾟ’★,｡･:*:･ﾟ’☆")
        elif choose == 'Q':
            break

        player.save()


def pow_check():
    import hashlib
    prefix = secrets.token_hex(4)
    print("=== PoW (Proof of Work) ===")
    print(f"sha256('{prefix}' + INPUT).hexdigest().startswith('000000')")
    INPUT = input("Input: ")
    if hashlib.sha256((prefix+INPUT).encode()).hexdigest().startswith("000000"):
        return
    else:
        print('verify failed')
        exit()


if __name__ == '__main__':
    def handler(signum, frame):
        print("timeout")
        if player != None:
            player.save()
        exit()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)  # 5 minutes

    pow_check()
    game()
