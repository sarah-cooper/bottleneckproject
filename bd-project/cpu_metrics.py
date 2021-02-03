#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 01:08:24 2019

@author: masudulhasanmasudb
"""
import subprocess,time

output_file = open("cpu_stat.txt","a+")

#comm_ss = ['iostat']
#while(1):
#    ss_proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
#    line_in_ss = str(ss_proc.stdout.read())
#    print (line_in_ss)
##    print(time.ctime() + "\n")
##    output_file.write(time.ctime() + "\n")
##    output_file.write(str(line_in_ss)+"\n\n")
##    output_file.flush()
#    time.sleep(1)


#    
    
import psutil

while(1):
    #print(time.ctime() + "\n")
    output_file.write(time.ctime() + "\n")
    output_file.write(str(psutil.cpu_percent())+"\n")
    output_file.write(str(psutil.virtual_memory())+"\n")
    output_file.write(str(psutil.cpu_times_percent(percpu=False))+"\n")
    output_file.write(str(psutil.cpu_percent(percpu=True))+"\n\n")
    output_file.flush()
    time.sleep(1)



# gives a single float value
#print(psutil.cpu_percent())
## gives an object with many fields
#print(psutil.virtual_memory())
#print(psutil.cpu_times())
#
#for x in range(3):
#    print(psutil.cpu_times_percent(interval=1, percpu=False))
#
#for x in range(3):
#    print(psutil.cpu_percent(interval=1,percpu=True))    
# you can convert that object to a dictionary 
#dict(psutil.virtual_memory()._asdict())
#
#import os
#
#CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))
#
##print results
#print("CPU Usage = " + CPU_Pct)    
