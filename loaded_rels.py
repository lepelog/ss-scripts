#!/bin/python3 -u
import json
from typing import Dict
import sys
import dolphin_memory_engine

with open('new_actor_list.json') as f:
    actor_list = json.load(f)
    for entry in actor_list:
        if 'ghidra_base' in entry:
            entry['ghidra_base'] = int(entry['ghidra_base'], 16)
            entry['ghidra_size'] = int(entry['ghidra_size'], 16)
            entry['ghidra_end'] = entry['ghidra_base'] + entry['ghidra_size']

def read_loaded_rels() -> Dict[int, int]:
    DYLINK_REL_INFO = dolphin_memory_engine.read_word(0x805750e8)
    # actor_id -> address
    addresses = {}
    for i in range(703):
        dylink_ptr = dolphin_memory_engine.read_word(DYLINK_REL_INFO + i * 4)
        if dylink_ptr != 0:
            # check if it's loaded
            base_addr = dolphin_memory_engine.read_word(dylink_ptr + 0x14)
            if base_addr != 0:
                code_start = dolphin_memory_engine.read_word(base_addr + 0x34)
                addresses[i] = code_start
    return addresses

def try_convert_addr(str_addr: str):
    if str_addr.lower().startswith('0x'):
        str_addr = str_addr.lstrip('0x')
    return int(str_addr, 16)

def try_convert_from_ghidra_to_dolphin(addr, loaded_rels):
    # check ghidra ranges
    for id, entry in enumerate(actor_list):
        if 'ghidra_base' in entry and addr >= entry['ghidra_base'] and addr <= entry['ghidra_end']:
            if game_addr := loaded_rels.get(id):
                print(f"converted from ghidra to dolphin: {addr - entry['ghidra_base'] + game_addr:X}")
            else:
                print(f"{entry['name']} is not loaded!")
            return True
    return False

def try_convert_from_dolphin_to_ghidra(addr, loaded_rels):
    for id, rel_addr in loaded_rels.items():
        entry = actor_list[id]
        if 'ghidra_base' in entry and addr >= rel_addr and addr <= rel_addr + entry['ghidra_size']:
            print(f"converted from dolphin to ghidra ({entry['name']}): {addr - rel_addr + entry['ghidra_base']:X}")
            return True
    return False

def print_use():
    print('actions:')
    print('list, lists all loaded rels with their base address')
    print('(some address), either give a ghidra or game address, both are checked')
    sys.exit(1)

def main():
    dolphin_memory_engine.hook()
    if len(sys.argv) < 2:
        print_use()
    action = sys.argv[1]
    loaded = read_loaded_rels()
    if action == 'list':
        for id, addr in loaded.items():
            print(f"{id}:{actor_list[id]['name']}:{actor_list[id]['obj_name']}:{actor_list[id]['rel_name']}:{addr:X}")
    elif action.lower().startswith('0x') or action.isalnum():
        addr = try_convert_addr(action)
        if not try_convert_from_dolphin_to_ghidra(addr, loaded) and not try_convert_from_ghidra_to_dolphin(addr, loaded):
            print("can't convert this address in any way!")
    else:
        print_use()

        

if __name__ == '__main__':
    main()

