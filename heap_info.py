#!/bin/python3 -u
from util import print_all_allocs, print_free_used
import dolphin_memory_engine

def main():
    dolphin_memory_engine.hook()
    # print('DYLINK')
    # print_free_used(0x80575c44)
    # print('WORK1')
    # print_free_used(0x805751a8)
    # print('WORK2')
    # print_free_used(0x805751ac)
    # print('ACTOR[0]')
    # print_free_used(0x805cb078)
    print('ROOT1')
    print_free_used(0x805a0738)
    print_all_allocs(0x805a0738)
    print('ROOT2')
    print_free_used(0x805a073C)
    print_all_allocs(0x805a073C)
    print('SYS_ROOT1')
    print_free_used(0x8057522c)
    print_all_allocs(0x8057522c)
    print('SYS_ROOT2')
    print_free_used(0x80575230)
    print_all_allocs(0x80575230)
    print('LAYOUT_RES')
    print_free_used(0x805751c0)
    print_all_allocs(0x805751c0)
        

if __name__ == '__main__':
    main()
