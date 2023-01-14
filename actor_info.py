#!/bin/python3 -u
import json
import struct
from util import iter_pointers, read_allocator_ptr
import dolphin_memory_engine

E_BC = 382
E_SM = 341
E_KS = 365
ITEM = 641

with open('new_actor_list.json') as f:
    ACTOR_LIST = json.load(f)

def main():
    dolphin_memory_engine.hook()
    heap = read_allocator_ptr(0x805cb078)
    for node_ptr in iter_pointers(heap["usedH"]):
        actor_ptr = node_ptr + 0x10
        actor_name = struct.unpack('>H', dolphin_memory_engine.read_bytes(actor_ptr + 8, 2))[0]
        if actor_name >= len(ACTOR_LIST):
            continue
        if actor_name in (ITEM,) or True:
            # actor_flags = dolphin_memory_engine.read_word(actor_ptr + 0xd8)
            # dolphin_memory_engine.write_word(actor_ptr + 0xd8, 0)
            print(f"{ACTOR_LIST[actor_name]['name']}:{dolphin_memory_engine.read_word(actor_ptr + 4):08X}")
            # print(f"{ACTOR_LIST[actor_name]['name']}:{actor_flags:08X}")

if __name__ == '__main__':
    main()
