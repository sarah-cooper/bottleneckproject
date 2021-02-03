#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:23:59 2019

@author: masudulhasanmasudb
"""

import threading
import time

class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        
    def run(self):
        print("\nStarting " + str(self.name))
        run_command(self.name)
        print("\nExiting " + str(self.name))


def run_command(index):
    present_time = time.time()
    read_so_far = 0
    file_number = (int(index)%10)
    with open('/fsx/files/large_file_'+str(file_number), 'rb') as f: 
        while True: 
            piece = f.read(1024) 
            if not piece: 
                break
        f.close()


while(1):
    jobs = []
    for x in range(32):
        thread1 = myThread(x)
        thread1.start()
        jobs.append(thread1)
    for t in jobs:
        t.join()            