#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 03:14:06 2019

@author: masudulhasanmasudb
"""

def generate_big_random_letters(filename,size):
    """
    generate big random letters/alphabets to a file
    :param filename: the filename
    :param size: the size in bytes
    :return: void
    """
    import random
    import string

    chars = ''.join([random.choice(string.ascii_letters) for i in range(size)]) #1


    with open(filename, 'w') as f:
        for x in range(1024):
            f.write(chars)
    pass

import time,sys

file_name= sys.argv[1] 
if __name__ == '__main__':
    for x in range(1):
        generate_big_random_letters(str(file_name),1024*1024)
