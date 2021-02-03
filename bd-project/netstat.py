#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:00:28 2019

@author: masudulhasanmasudb
"""
import subprocess,time

output_file = open("netstat.txt","a+")

comm_ss = ['netstat', '-st']
while(1):
    ss_proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
    line_in_ss = str(ss_proc.stdout.read())
#    print (line_in_ss)
#    print(time.ctime() + "\n")
    output_file.write(time.ctime() + "\n")
    output_file.write(str(line_in_ss)+"\n\n")
    output_file.flush()
    time.sleep(1)

#globus-url-copy -vb gsiftp://oasis-dm.sdsc.xsede.org:2811/~/gridftp_xfer.log gsiftp://gridftp.bridges.psc.edu:2811/pylon5/ci560np/masud/gridftp_xfer.log

