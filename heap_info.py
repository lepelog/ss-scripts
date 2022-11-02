#!/bin/python3 -u
import json
from typing import Dict
import sys
import collections
import struct
import dolphin_memory_engine

def unpack(fields, formatstr, item):
    return (
        collections.namedtuple("_", fields)
        ._make(struct.unpack(formatstr, item))
        ._asdict()
    )

def read_alloc_node(at):
    b=dolphin_memory_engine.read_bytes(at, 0x10)
    return unpack('magic pad size prev next', '>HHIII', b)

def read_allocator_ptr(at):
    ptr = dolphin_memory_engine.read_word(at)
    if ptr != 0:
        return read_allocator(ptr)

def read_allocator(at):
    ptr = dolphin_memory_engine.read_word(at + 0x10)
    b = dolphin_memory_engine.read_bytes(ptr + 0x3C, 0x10)
    return unpack('freeH freeT usedH usedT', '>IIII', b)

def get_sizes(node_head_ptr):
    allocations = []
    while node_head_ptr != 0:
        # print(f"{node_head_ptr:X}")
        node = read_alloc_node(node_head_ptr)
        allocations.append(node['size'])
        node_head_ptr = node['next']
    return allocations

def print_free_used(heap_ptr):
    heap = read_allocator_ptr(heap_ptr)
    print(f"free : {sum(get_sizes(heap['freeH'])):X}")
    used_allocs = get_sizes(heap['usedH'])
    print(f"used : {sum(used_allocs):X}")
    print(f"count: {len(used_allocs)}")

def main():
    dolphin_memory_engine.hook()
    print('DYLINK')
    print_free_used(0x80575c44)
    print('WORK1')
    print_free_used(0x805751a8)
    print('WORK2')
    print_free_used(0x805751ac)
    print('ACTOR[0]')
    print_free_used(0x805cb078)
        

if __name__ == '__main__':
    main()
