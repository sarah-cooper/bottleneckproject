#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 21:45:36 2019

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
        for x in range(5):
            f.write(chars)
    pass

if __name__ == '__main__':
    for x in range(1):
        generate_big_random_letters("tmp_file_"+str(x)+".txt",1024*1024)