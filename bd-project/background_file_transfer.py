#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 00:32:55 2019

@author: masudulhasanmasudb
"""

import threading
import time
from subprocess import PIPE, Popen

exitFlag = 0


# out_file = open("time_stat_for_2_process", "a+")
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("\nStarting " + self.name)
        run_command(self.threadID, self.counter)
        print("\nExiting " + self.name)


def run_command(index, delay):
    comm_ss = ['globus-url-copy','-vb','file:///oasis-dm.sdsc.xsede.org:2811//oasis/projects/nsf/sub102/masud/file_directory/another_tmp_file', 
               'gsiftp://gridftp.bridges.psc.edu:2811/pylon5/ci560np/masud/tmp_file_'+index]
    proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
    proc.communicate()


counter = 5
i = 1
first_start_time = time.time()
jobs = []

for x in range(1):
    thread1 = myThread(i, x, 10)
    thread1.start()
    jobs.append(thread1)
for t in jobs:
    t.join()
