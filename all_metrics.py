
import psutil
import time
import subprocess
import socket
import traceback
import os.path
from subprocess import Popen,PIPE
import random
import string
import threading
import ast
import sys

#global Variables
sleep_time = .1
total_time = 600 #1800
label = int(sys.argv[1])
pid = 0
per = False
initial_time = time.time()


class fileTransferThread(threading.Thread):
    def __init__(self, name,label):
        threading.Thread.__init__(self)
        self.name = name
        self.label = str(label)
        
    def run(self):
        print("\nStarting " + self.label)
        transfer_file(self.name)
        print("\nExiting " + self.label)

def transfer_file(stime):
    dic = os.listdir("/home/cc/to/")
    start_time = time.time()
    dist_ip = '10.52.3.12'
    port = 50505
    while True:
    	if int(time.time() - start_time) >= int(stime):
    		break
		for file_ in dic:
			if int(time.time() - start_time) >= int(stime):
				break
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.connect((dst_ip,port))
			
			filename = (file_+"\n").encode('utf-8')
			s.send(filename)
			time.sleep(1)
			
			with open("home/cc/to/"+file_,'rb') as fm:
				while True:
					l = fm.read(4096)
					if int(time.time() - start_time) >= int(stime):
						break
					if not l:
						break
					s.send(l)
			s.close()


class CPUThread(threading.Thread):
	def __init__(self,name,label):
		threading.Thread.__init__(self)
		self.name = name
		self.label = str(label)
	def run(self):
		#print('Starting CPU process ' + self.label)
		cpu_metrics(self.name,self.label)
		#print('Ending CPU process ' + self.label)

class NETThread(threading.Thread):
	def __init__(self,name,label):
		threading.Thread.__init__(self)
		self.name = name
		self.label = str(label)
	def run(self):
		#print('Starting NETWORK process ' + self.label)
		net_metrics(self.name,self.label)
		#print('Ending NETWORK process ' + self.label)

class MEMThread(threading.Thread):
	def __init__(self,name,label):
		threading.Thread.__init__(self)
		self.name = name
		self.label = str(label)
	def run(self):
		#print('Starting MEMORY process ' + self.label)
		mem_metrics(self.name,self.label)
		#print('Ending MEMORY process ' + self.label)

class IOThread(threading.Thread):
	def __init__(self,name,label):
		threading.Thread.__init__(self)
		self.name = name
		self.label = str(label)
	def run(self):
		#print('Starting IO process ' + self.label)
		io_metrics(self.name,self.label)
		#print('Ending IO process ' + self.label)
		
#CPU
def cpu_metrics(stime,label):
	OUTPUT= ''
	j =0
	while j < int(stime):
		OUTPUT = '\nData pt '+str(j)+':\t|\tTime: ' + time.ctime() + '\n'
		#cpu_times = psutil.cpu_times(percpu = per)
		cpu_per = psutil.cpu_percent(percpu = per) #good metric (changes with Lookbusy & Stress)
		cpu_tim_per = psutil.cpu_times_percent(percpu = per)
		cpu_stats = psutil.cpu_stats()
		cpu_freq = psutil.cpu_freq() #not per cpu
		#print(cpu_per)
		
		OUTPUT += '\tCPU Metrics ---> CPU User %Time: '+str(cpu_tim_per[0])+' | CPU Nice %Time: '+str(cpu_tim_per[1])+' | CPU System %Time: '+str(cpu_tim_per[2])+' | CPU Idle %Time: '+str(cpu_tim_per[3])+' | CPU Percent: '+str(cpu_per)+' | CPU Ctx Switches: ' + str(cpu_stats[0])+ ' | CPU Interrupts: '+str(cpu_stats[1])+' | CPU Soft Interrupts: '+str(cpu_stats[2])+' | CPU System Calls '+str(cpu_stats[3])+' | Current CPU Frequency: ' + str(cpu_freq[0]) +'\n'
		
		write_to_file('cpu_metrics.txt',OUTPUT)
		j+= 1
		time.sleep(sleep_time)


# network statistics
# cubic wscale, rto, rtt, ato, mss, pmtu, rcvmss, advmss, cwnd, bytes_sent, bytes_acked, bytes_received, segs_out, segs_in,data_segs_out, data_segs_in, send, lastsnd, lastrcv, lastack, pacing_rate,delivery_rate, delivered, app_limit busy, rcv_space, rcv_ssthrest, minrtt

def net_metrics(stime,label):
	OUTPUT = ''
	j = 0
	#write_to_file('CPU_metrics.txt','Running: '+str(label))
	dst_ip= '10.52.3.12'
	while k < int(stime):
		OUTPUT = '\nData pt '+str(k)+':\t|\tTime: ' + time.ctime() + '\n'
		
		net_mets = psutil.net_io_counters()
		
		OUTPUT += '\tNETWORK Metrics ---> Bytes Sent: '+str(net_mets[0])+' | Bytes Received: '+str(net_mets[1])+' | Packets Sent: '+str(net_mets[2])+' | Packets Received: '+str(net_mets[3])+' | Errors In: '+str(net_mets[4])+' | Errors Out: '+str(net_mets[5])+' | Drop In: '+str(net_mets[6])+' | Drop Out: '+str(net_mets[7])+' | '

		commands = ['ss','-t','-i','state','ESTABLISHED','dst',dst_ip]
		process = subprocess.Popen(commands,stdout= subprocess.PIPE)
		for i in range(3):
			string = str(process.stdout.readline())
			splt_wrd = string.strip("b'").strip("\\t").strip("\\n").strip()
			splt_wrd = splt_wrd.split()
			ind = 0
			for j in splt_wrd:
				if "rto" in j:
					OUTPUT += j + " | "
				elif "rtt" in j:
					index = j.find('/')
					OUTPUT += j[:index] + " | "
				elif "mss" in j:
					OUTPUT += j+ " | "
				elif "cwnd" in j:
					OUTPUT += j+ " | "
				elif "ssthresh" in j:
					OUTPUT += j+ " | "
				elif "bytes_acked" in j:
					OUTPUT += j+ " | "
				elif "segs_out" in j:
					OUTPUT += j+ " | "
				elif "segs_in" in j:
					OUTPUT += j+ " | "
				elif "send" in j:
					OUTPUT += j + splt_wrd[ind+1]+ " | "
				elif "pacing_rate" in j:
					OUTPUT += j + splt_wrd[ind+1]+ " | "
				elif "unacked" in j:
					OUTPUT += j + " | "
				elif "retrans" in j:
					OUTPUT += j + splt_wrd[ind+1]+ " | "
				elif "rcv_space" in j:
					OUTPUT += j + " | "
				ind +=1
			OUTPUT += '\n'
		write_to_file('net_metrics.txt',OUTPUT)
		k+=1
		time.sleep(sleep_time)
		

#Memory
def mem_metrics(stime,label):
	j = 0
	OUTPUT = ''
	#write_to_file('CPU_metrics.txt','Running: '+str(label))
	while j < int(stime):
		OUTPUT = '\nData pt '+str(j)+':\t|\tTime: ' + time.ctime() + '\n'
		vm = psutil.virtual_memory()
		sm = psutil.swap_memory()
		OUTPUT += '\tMEMORY Metrics ---> Total: '+str(vm[0]) +' | Available: ' + str(vm[1])+' | Percent: ' +str(vm[2])+' | Used: ' +str(vm[3])+' | Free: ' +str(vm[4])+' | Active: ' + str(vm[5])+' | Inactive: ' + str(vm[6])+' | Buffers: ' + str(vm[7]) +' | Cached: ' + str(vm[8])+' | Shared: ' + str(vm[9])+' | Slab: ' + str(vm[10]) + ' | ' + 'Swap Total: '+str(sm[0]) +' | Swap Available: ' + str(sm[2])+' | Swap Percent: ' + str(sm[1])+' | Swap Used: ' + str(sm[3])+' | Swap Free: ' +str(sm[4])+' | Swap Active: ' + str(sm[5]) + '\n'
		write_to_file('mem_metrics.txt',OUTPUT)
		j+=1
		time.sleep(sleep_time)

# Disk IO Metrics Using Psutil
# 8 Metrics Found
# Found for all disks (reads and writes + busy times)

# Device IO Metrics Using iostat
# includes CPU and Device metrics
# CPU: user, nice, system, iowait, steal, idle
# Device: tps, kB_read/s, kB_wrtn/s, kB_read, kB_wrtn
# 11 metrics found

def io_metrics(stime,label):
	j=0
	OUTPUT = ''
	#write_to_file('CPU_metrics.txt','Running: '+str(label))
	commands = ['iostat','-xd','1']
	process = subprocess.Popen(commands,stdout= subprocess.PIPE)
	while j < int(stime):
		OUTPUT = '\nData pt '+str(j)+':\t|\tTime: ' + time.ctime() + '\n'
		metric = psutil.disk_io_counters(perdisk = per)
		OUTPUT += '\tDISK Metrics ---> Read Count: ' +str(metric[0]) + ' | Read Bytes: ' + str(metric[2]) + ' | Read Times: ' + str(metric[4]) + ' | Read Merge: ' + str(metric[7])+ ' | Write Count: ' +str(metric[1]) + ' | Write Bytes: '+ str(metric[3]) + ' | Write Times: ' + str(metric[5]) + ' | Write Merge: ' + str(metric[8])+' | Busy Times: ' + str(metric[6]) + ' | '

		flag = 0
		while flag == 0:
			string = str(process.stdout.readline())
			string = string.split()
			if string[0][2:] == 'sda':
				OUTPUT += 'Device: '+string[0][2:] + ' | r/s: ' + string[1] + ' | w/s: ' + string[2] + ' | rkB/s: ' + string[1] + ' | wkB/s: ' + string[2] + ' | rrqm/s: ' + string[3] + ' | wrqm/s: '+ string[4] + ' | %rrqm: ' + string[5] + ' | %wrqm: ' + string[6] + ' | r_await: ' + string[7] + ' | w_await: '+ string[8] + ' | aqu-sz: ' + string[9] + ' | rareq-sz: ' + string[10] + ' | wareq-sz: ' + string[11] + ' | %util: '+ string[13] + '\n\n'
				flag = 1
			
		write_to_file('io_metrics.txt',OUTPUT)
		j+=1
		time.sleep(sleep_time)
		
def write_to_file(filename,output):
	with open(filename,'a+') as f:
		f.write(output)


#main
def main():
	label = int(sys.argv[1])
	Threads = []
	inital_time = time.time()
	print('starting Main: '+str(sys.argv[1]))
	
	write_to_file('cpu_metrics.txt','Running: '+str(label))
	write_to_file('net_metrics.txt','Running: '+str(label))
	write_to_file('mem_metrics.txt','Running: '+str(label))
	write_to_file('io_metrics.txt','Running: '+str(label))
	
	cputhread = CPUThread(total_time,label)
	netthread = NETThread(total_time,label)
	memthread = MEMThread(total_time,label)
	iothread = IOThread(total_time,label)
	cputhread.start()
	netthread.start()
	memthread.start()
	iothread.start()
	Threads.append(cputhread)
	Threads.append(netthread)
	Threads.append(memthread)
	Threads.append(iothread)
	
	file_transfer = fileTransferThread(total_time,label)
	file_transfer.start()
	
	for j in Threads:
		j.join()
	

	print('Ending Main: '+str(sys.argv[1]))
	
if __name__ == '__main__':
	main()

