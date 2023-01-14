#!/bin/python3 -u
import json
import struct
from typing import Dict
import sys
import dolphin_memory_engine

from util import read_null_term_string

dolphin_memory_engine.hook()

def dme_read_ushort(ptr):
    b = dolphin_memory_engine.read_bytes(ptr, 2)
    return struct.unpack('>H', b)[0]

class EventSystemActorRelation:
    def __init__(self, ptr) -> None:
        self.ptr = ptr
    
    @property
    def done_indices_flags(self):
        return dolphin_memory_engine.read_word(self.ptr + 0xd4)
    
    @property
    def advance_condition(self):
        return dolphin_memory_engine.read_word(self.ptr + 0xd8)
    
    @property
    def advance_signal(self):
        return dolphin_memory_engine.read_word(self.ptr + 0xdc)
    
    @property
    def actor_vtbl(self):
        actor_ptr = dolphin_memory_engine.read_word(self.ptr + 0x3C)
        return dolphin_memory_engine.read_word(actor_ptr + 0x60)

    @property
    def event_actor_entry(self):
        return EventActorEntry(dolphin_memory_engine.read_word(self.ptr + 8))
    
    @property
    def event_reloc_info(self):
        event_table_ptr = dolphin_memory_engine.read_word(self.ptr + 0xCC)
        event_reloc_info_ptr = dolphin_memory_engine.read_word(event_table_ptr + 0x148)
        return EventRelocInfo(event_reloc_info_ptr)

    def step_long_name(self, idx):
        ptr = self.event_reloc_info.step1_ptr + (self.event_actor_entry.step1_start_idx + idx) * 0x1C
        name = dolphin_memory_engine.read_bytes(ptr, 16)
        return read_null_term_string(name)

    def step_command(self, idx):
        ptr = self.event_reloc_info.step2_ptr + (self.event_actor_entry.step1_start_idx + idx) * 0xC
        return dolphin_memory_engine.read_bytes(ptr, 4).decode('ASCII')

    @property
    def step1idx(self):
        return dolphin_memory_engine.read_word(self.ptr + 0x48)
    
    @property
    def actor_name(self):
        b = dolphin_memory_engine.read_bytes(self.ptr + 0xc, 32)
        return read_null_term_string(b)

class EventActorEntry:
    def __init__(self, ptr) -> None:
        self.ptr = ptr
    
    @property
    def step1_start_idx(self):
        return dme_read_ushort(self.ptr + 0x24)

class EventRelocInfo:
    def __init__(self, ptr) -> None:
        self.ptr = ptr
    
    @property
    def step1_ptr(self):
        return dolphin_memory_engine.read_word(self.ptr + 0x10)
    
    @property
    def step2_ptr(self):
        return dolphin_memory_engine.read_word(self.ptr + 0x14)

if __name__ == '__main__':
    addr = 0x805a3178
    actors = []
    for _ in range(5):
        actors.append(EventSystemActorRelation(addr))
        addr += 0xE0
    
    for a in actors:
        if a.actor_name != "":
            print()
            print(a.actor_name)
            print(f"{a.actor_vtbl:X}")
            print(f"step {a.step_long_name(a.step1idx)}")
            print(f"cmd  {a.step_command(a.step1idx)}")
            print(f"step {a.step1idx}")
            print(f"advc {a.advance_condition}")
            print(f"advs {a.advance_signal}")
            print(f"done {a.done_indices_flags}")
