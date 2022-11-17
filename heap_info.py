#!/bin/python3 -u
from util import print_free_used
import dolphin_memory_engine

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
