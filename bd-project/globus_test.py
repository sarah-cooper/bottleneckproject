#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:00:28 2019

@author: masudulhasanmasudb
"""
import subprocess,time
import time,sys

file_name= sys.argv[1] 
output_file = open("file_transfer_stat.txt","a+")
#comm_ss = ['globus-url-copy','-vb','gsiftp://oasis-dm.sdsc.xsede.org:2811//oasis/projects/nsf/sub102/masud/file_directory/tmp_file', 'gsiftp://gridftp.bridges.psc.edu:2811/pylon5/ci560np/masud/gridftp_xfer.log']
comm_ss = ['globus-url-copy','-vb','file:///oasis/projects/nsf/sub102/masud/file_directory/'+str(file_name), 'gsiftp://br034.dmz.bridges.psc.edu:2811/pylon5/ci560np/masud/big_file_1']
strings = ""
proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
output_file.write("start time = "+time.ctime() + "\n")
start_time = time.time()
while(True):
	line = str(proc.stdout.readline()).replace("\r", "\n")
	#print(time.ctime() + "\n")
	#print(line)
	#line = proc.stdout.readline()
	strings+= line
	#print(line)
           #speed = self.get_filetransfer_complete(line)
	if not line.decode("utf-8"):
		break
strings.replace("\r", "\n")
#print(strings)
output_file.write(strings+"\n\n")
output_file.write("end time = "+time.ctime() + "\n")
output_file.write("total time = " + str(int(time.time() - start_time))+"\n\n")
output_file.flush()


#line_in_ss = str(ss_proc.stdout.read())
#print(time.ctime() + "\n")

#globus-url-copy -vb gsiftp://oasis-dm.sdsc.xsede.org:2811//oasis/scratch-comet/masud/temp_project/file_directory/tmp_file gsiftp://gridftp.bridges.psc.edu:2811/pylon5/ci560np/masud/gridftp_xfer.log
#globus-url-copy -vb gsiftp://oasis-dm.sdsc.xsede.org:2811/~/gridftp_xfer.log gsiftp://gridftp.bridges.psc.edu:2811/pylon5/ci560np/masud/gridftp_xfer.log

