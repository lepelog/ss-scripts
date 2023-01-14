#!/bin/python3 -u
import json
from typing import Dict, Iterator
import sys
import collections
import struct
import dolphin_memory_engine
from dataclasses import dataclass

def unpack(fields, formatstr, item):
    return (
        collections.namedtuple("_", fields)
        ._make(struct.unpack(formatstr, item))
        ._asdict()
    )

def read_alloc_node(at: int):
    b=dolphin_memory_engine.read_bytes(at, 0x10)
    return unpack('magic pad size prev next', '>HHIII', b)

@dataclass
class Node:
    magic: int
    pad: int
    size: int
    prev: int
    next: int

def read_allocator_ptr(at:int ):
    ptr = dolphin_memory_engine.read_word(at)
    if ptr != 0:
        return read_allocator(ptr)

def read_allocator(at: int):
    ptr = dolphin_memory_engine.read_word(at + 0x10)
    b = dolphin_memory_engine.read_bytes(ptr + 0x3C, 0x10)
    return unpack('freeH freeT usedH usedT', '>IIII', b)

def iter_pointers(node_head_ptr: int) -> Iterator[int]:
    while node_head_ptr != 0:
        yield node_head_ptr
        # print(f"{node_head_ptr:X}")
        node = read_alloc_node(node_head_ptr)
        node_head_ptr = node['next']

def iter_nodes(node_head_ptr: int) -> Iterator[Node]:
    while node_head_ptr != 0:
        # print(f"{node_head_ptr:X}")
        node = read_alloc_node(node_head_ptr)
        node_head_ptr = node['next']
        yield Node(**node)

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

def print_all_allocs(heap_ptr):
    heap = read_allocator_ptr(heap_ptr)
    for node in iter_nodes(heap['usedH']):
        print(node)

def read_null_term_string(s: bytes) -> str:
    return s.split(b'\x00', 1)[0].decode('ASCII')
