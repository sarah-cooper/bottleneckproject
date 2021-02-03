#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 22:08:51 2019

@author: masudulhasanmasudb
"""
import threading
import time
from subprocess import PIPE, Popen
import subprocess
import sys, traceback
import os.path
from subprocess import check_output

## HIGH I/0 = 1 i/o==6000
## HIGH disk load = 2 disk load=32
## HIGH disk load = 3 disk load=16
## HIGH disk load = 4 disk load=8
## HIGH disk load = 5 disk load=4
## HIGH memory load = 6 
## packet drop = 7 probability = .01
##packet delay = 8 100ms 20ms
label_value = 8
should_run = True
pid = 0
class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        
    def run(self):
        print("\nStarting " + self.name)
        run_command(self.name)
        print("\nExiting " + self.name)


def run_command(index):
    present_time = time.time()
    read_so_far = 0
    with open('temp_files/tmp_file_'+index+'.txt', 'rb') as f: 
        while True: 
            piece = f.read(1024) 
            if not piece: 
                break

class fileTransferThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        
    def run(self):
        print("\nStarting " + self.name)
        transfer_file(self.name)
        print("\nExiting " + self.name)

         
def transfer_file(i):
    global pid
    output_file = open("file_transfer_stat.txt","a+")
    comm_ss = ['globus-url-copy', '-vb','file:///fsx/files/large_file_'+str(i), 'ftp://172.31.21.192:50505/home/ubuntu/large_file']
#    comm_ss = ['globus-url-copy', '-vb','file:///fsx/files/test_file', 'ftp://172.31.21.192:50505/home/ubuntu/large_file']
    strings = ""
    proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
    pid = check_output(['pidof', '-s', 'globus-url-copy'])
    print(check_output(['pidof', '-s','globus-url-copy']))
    output_file.write("start time = "+time.ctime() + "\n")
    start_time = time.time()
    while(True):
        line = str(proc.stdout.readline()).replace("\r", "\n")
        strings+= line
        if not line.decode("utf-8"):
            break
        strings.replace("\r", "\n")
        output_file.write(strings+"\n\n")
        output_file.write("end time = "+time.ctime() + "\n")
        output_file.write("total time = " + str(int(time.time() - start_time))+"\n\n")
        output_file.flush()

def set_thread_value(y):
    global current_Thread_number
    current_Thread_number = y
    

class readbackgroundThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()

    def run(self):
#        global current_Thread_number = 1
        for y in range(1,33):
            jobs = []
            self.lock.acquire()
            try:
                print('Acquired lock')
                set_thread_value(y)
            finally:
                self.lock.release()
            
            for x in range(y):
                thread1 = myThread(str(x))
                thread1.start()
                jobs.append(thread1)
            for t in jobs:
                t.join()    

def process_mds_rpc(mdt_path):
    proc = Popen(['cat', mdt_path+"/import"], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    res_parts = res.split("\n")
    for metric_line in res_parts:
        if "avg_waittime:" in metric_line:
            s_index = metric_line.find(":")
            e_index = metric_line.find("usec")
            avg_waittime = float(metric_line[s_index+1:e_index].strip())
#            print(avg_waittime)
            
        if "inflight:" in metric_line:
            s_index = metric_line.find(":")
            inflight = float(metric_line[s_index+1:].strip())
#            print(inflight)
        
        if "unregistering:" in metric_line:
            s_index = metric_line.find(":")
            unregistering = float(metric_line[s_index+1:].strip())
#            print(unregistering)
            
        if "timeouts:" in metric_line:
            s_index = metric_line.find(":")
            timeouts = float(metric_line[s_index+1:].strip())
#            print(timeouts)
    return avg_waittime, inflight, unregistering, timeouts

def collect_system_metrics(pid):
    print(pid)
    proc = Popen(['cat', '/proc/'+str(pid).strip()+'/io'], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    res_parts = res.split("\n")
    value_list = []
    for line in res_parts:
        if len(line.strip())>0:
#            print(line)
            index= line.rfind(":")
            value = int(line[index+1:].strip())
#            print(value)
            value_list.append(value)
    
    proc = Popen(['cat', '/proc/'+str(pid).strip()+'/stat'], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    res_parts = res.split(" ")
    for line in res_parts:
        if len(line.strip())>0:
#            print(line)
            try:
                value = int(line.strip())
                value_list.append(value)
            except:
                traceback.print_exc()
#    print(value_list)
    proc = Popen(['ps','-p', str(pid).strip(), '-o',  '%cpu,%mem'], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    res_parts = res.split("\n")
    for line in res_parts:
        if len(line.strip())>0:
            if "%CPU" not in line:
                parts = line.split(" ")
#                print(parts)
                for x in parts:
                    if len(x.strip())>0:
                        value_list.append(float(x))
    return value_list


def collect_stat():
    proc = Popen(['ls', '-l', '/proc/fs/lustre/osc'], universal_newlines=True, stdout=PIPE)
    res = proc.communicate()[0]
    parts = res.split("\n")
    for x in range(1, len(parts)):
        ost_name_parts = parts[x].split(" ")
        if "fsx-OST0009" in ost_name_parts[len(ost_name_parts) - 1]:
            OST_name = ost_name_parts[len(ost_name_parts) - 1]
            break
    ost_path = '/proc/fs/lustre/osc/' + OST_name
    mdt_path = "/proc/fs/lustre/mdc/fsx-MDT0000-mdc-ffff88037f720800"
    
    dst_ip = "172.31.21.192"
    comm_ss = ['ss', '-t', '-i', 'state', 'ESTABLISHED', 'dst', dst_ip]
    is_controller_port = True
    
    total_string = ""
    start = time.time()
    initial_time = time.time()
    total_rtt_value = 0
    total_pacing_rate = 0
    is_first_time = True
    avg_wait_time = 0
    total_wait_time = 0
    total_cwnd_value = 0
    total_rto_value = 0
    byte_ack = 0
    byte_ack_so_far = 0
    segs_out = 0
    seg_out_so_far = 0
    segs_in = 0
    seg_in_so_far = 0
    retrans = 0
    total_ssthresh_value =0
    total_ost_read = 0
    send = 0
    unacked = 0
    rcv_space = 0
    
    prev_req_wait_time = -1
    prev_active_req = -1
    prev_red_bytes = -1
    prev_ost_read = -1
    prev_ost_connect = -1
    prev_ost_statfs = -1
    prev_ldlm_cancel = -1
    prev_obd_ping = -1
    
    avg_req_number = 0
    total_req_number = 0
    total_read_bytes = 0
    total_ost_read = 0
    total_ost_connect = 0
    total_ost_statfs = 0
    total_ldlm_cancel = 0
    total_obd_ping = 0
    
    total_pending_page = 0
    total_pending_rpc = 0
    total_mss_value = 0
    
    mds_prev_req_wait_time, mds_prev_active_req, prev_mds_getattr, prev_mds_close, prev_mds_readpage, prev_mds_connect,\
    prev_mds_get_root, prev_mds_statfs, mds_prev_ldlm_cancel, mds_prev_obd_ping = (-1,)*10
        
    mds_total_req_wait_time, mds_total_active_req, total_mds_getattr, total_mds_close, total_mds_readpage, total_mds_connect,\
    total_mds_get_root, total_mds_statfs, mds_total_ldlm_cancel, mds_total_obd_ping = (0,)*10
    
    prev_md_close, prev_md_getattr, prev_md_intent_lock,\
    prev_md_read_page, prev_md_revalidate_lock = (-1,)*5
        
    total_md_getattr, total_md_close, total_md_readpage,\
    total_md_intent_lock, total_md_revalidate_lock = (0,)*5
    
    time_diff = 0
    epoc_time = 0
    has_transfer_started = False
    
    sleep_time = .1
    
    epoc_count = 0
    main_output_string = ""

    while(1):
                    ### NETWORK METRICS ###
        try:
            ss_proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
            line_in_ss = str(ss_proc.stdout.read())
            if line_in_ss.count("172.31.21.192")==2:
                if (is_first_time):
                    initial_time = time.time()
                    is_first_time = False
                    
                parts = line_in_ss.split("\n")
                
                time_diff+=1
                epoc_time+=1
    
                for x in range(len(parts)):
                    if "172.31.21.192" in parts[x] and "50505" not in parts[x]:
                        
                        first_parts = parts[x].split(" ")
                        first_list = []
                        for item in first_parts:
                            if len(item.strip())>0:
                                first_list.append(item)
                        send_buffer_value = int(first_list[1].strip())
                        
                        if (is_first_time):
                            initial_time = time.time()
                            is_first_time = False
                        
                        metrics_line = parts[x+1].strip("\\t").strip()
                        metrics_parts = metrics_line.split(" ")
                #        print(metrics_parts)
                        for y in range(len(metrics_parts)):
                            
                            if "rto" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                total_rto_value+=value
                            
                            if "rtt" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                e_index = metrics_parts[y].find("/")
                                value = float(metrics_parts[y][s_index+1:e_index])
                                total_rtt_value+=value
                            
                            if "mss" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                total_mss_value+=value
                                
                            if "cwnd" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                total_cwnd_value+=value
                            
                            if "ssthresh" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                total_ssthresh_value+=value
                            
                            if "bytes_acked" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])                     
                                byte_ack+=(value-byte_ack_so_far)
                                byte_ack_so_far = value
                                
                            if "segs_out" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                segs_out+=(value-seg_out_so_far)
                                seg_out_so_far = value
                            
                            if "segs_in" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                segs_in+=(value-seg_in_so_far)
                                seg_in_so_far = value
                                
                            if "send" in metrics_parts[y]:
#                                match = re.compile("[^\W\d]").search(s)
#                                index = metrics_parts[y+1].find("Mbps")
#                                value = float(metrics_parts[y+1][:index])
                                value = metrics_parts[y+1].strip()
                                send=value
                                
                            if "pacing_rate" in metrics_parts[y]:
#                                index = metrics_parts[y+1].find("Mbps")
#                                p_rate = float(metrics_parts[y+1][:index])
                                value = metrics_parts[y+1].strip()
                                total_pacing_rate=value
                            
                            if "unacked" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                unacked += value
                            
                            if "retrans" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                e_index = metrics_parts[y].find("/")
                                value = float(metrics_parts[y][s_index+1:e_index])
                                retrans += value
                            
                            if "rcv_space" in metrics_parts[y]:
                                s_index = metrics_parts[y].find(":")
                                value = float(metrics_parts[y][s_index+1:])
                                rcv_space += value
    
    ### OST METRICS ###
    
                        
            proc = Popen(['cat', ost_path+"/stats"], universal_newlines=True, stdout=PIPE)
            res = proc.communicate()[0]
            res_parts = res.split("\n")
            for metric_line in res_parts:
                if "req_waittime" in metric_line:
                    tokens = str(metric_line).split(" ")
                    wait_time = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_req_wait_time == -1):
                        prev_req_wait_time = wait_time
                    elif(time_diff>1):
                        diff = wait_time - prev_req_wait_time
                        total_wait_time+=(diff/(1000000))
                        prev_req_wait_time = wait_time
    
                if "req_active" in metric_line:
                    tokens = str(metric_line).split(" ")
                    req_number = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_active_req== -1):
                        prev_active_req = req_number
                    elif(time_diff>1):
                        diff = req_number - prev_active_req
                        total_req_number+= diff
                        prev_active_req = req_number
                        
                if "read_bytes" in metric_line:
                    tokens = str(metric_line).split(" ")
                    read_bytes = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_red_bytes == -1):
                        prev_red_bytes = read_bytes
                    elif(time_diff>1):
                        diff = read_bytes - prev_red_bytes
                        total_read_bytes+= (diff/(1024*1024))
                        prev_red_bytes = read_bytes
                        
                if "ost_read" in metric_line:
                    tokens = str(metric_line).split(" ")
                    ost_read = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_ost_read == -1):
                        prev_ost_read = ost_read
                    elif(time_diff>1):
                        diff = ost_read - prev_ost_read
                        total_ost_read+= (diff/(1000000))
                        prev_ost_read = ost_read
               
                if "ost_connect" in metric_line:
                    tokens = str(metric_line).split(" ")
                    ost_connect = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_ost_read == -1):
                        prev_ost_connect = ost_connect
                    elif(time_diff>1):
                        diff = ost_connect - prev_ost_connect
                        total_ost_connect+= (diff/(1000000))
                        prev_ost_connect = ost_connect
                        
                if "ost_statfs" in metric_line:
                    tokens = str(metric_line).split(" ")
                    ost_statfs = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_ost_statfs == -1):
                        prev_ost_statfs = ost_statfs
                    elif(time_diff>1):
                        diff = ost_statfs - prev_ost_statfs
                        total_ost_statfs+= (diff/(1000000))
                        prev_ost_statfs = ost_statfs
                        
                if "ldlm_cancel" in metric_line:
                    tokens = str(metric_line).split(" ")
                    ldlm_cancel = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_ldlm_cancel == -1):
                        prev_ldlm_cancel = ldlm_cancel
                    elif(time_diff>1):
                        diff = ldlm_cancel - prev_ldlm_cancel
                        total_ldlm_cancel+= (diff/(1000000))
                        prev_ldlm_cancel = ldlm_cancel
                        
                if "obd_ping" in metric_line:
                    tokens = str(metric_line).split(" ")
                    obd_ping = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_obd_ping == -1):
                        prev_obd_ping = obd_ping
                    elif(time_diff>1):
                        diff = obd_ping - prev_obd_ping
                        total_obd_ping+= (diff/(1000000))
                        prev_obd_ping = obd_ping
                    
            proc = Popen(['cat', ost_path+"/rpc_stats"], universal_newlines=True, stdout=PIPE)
            res = proc.communicate()[0]
            res_parts = res.split("\n")
            for metric_line in res_parts:
                if "pending read pages" in metric_line:
                    index = metric_line.find(":")
                    value = float(metric_line[index+1:])
                    total_pending_page+=value
    
                if "read RPCs in flight" in metric_line:
                    index = metric_line.find(":")
                    value = float(metric_line[index+1:])
                    total_pending_rpc+=value
    
    ### MDT METRICS ###
            
            
            proc = Popen(['cat', mdt_path+"/stats"], universal_newlines=True, stdout=PIPE)
            res = proc.communicate()[0]
            res_parts = res.split("\n")
            for metric_line in res_parts:
                if "req_waittime" in metric_line:
                    tokens = str(metric_line).split(" ")
                    wait_time = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and mds_prev_req_wait_time == -1):
                        mds_prev_req_wait_time = wait_time
                    elif(time_diff>1):
                        diff = wait_time - mds_prev_req_wait_time
                        mds_total_req_wait_time+=(diff/(1000000))
                        mds_prev_req_wait_time = wait_time
    
                if "req_active" in metric_line:
                    tokens = str(metric_line).split(" ")
                    req_number = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and mds_prev_active_req== -1):
                        mds_prev_active_req = req_number
                    elif(time_diff>1):
                        diff = req_number - mds_prev_active_req
                        mds_total_active_req+= diff
                        mds_prev_active_req = req_number
                        
                if "mds_getattr" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_getattr = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_getattr == -1):
                        prev_mds_getattr = mds_getattr
                    elif(time_diff>1):
                        diff = mds_getattr - prev_mds_getattr
                        total_mds_getattr+= (diff/(1000000))
                        prev_mds_getattr = mds_getattr
                
                if "mds_close" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_close = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_close == -1):
                        prev_mds_close = mds_close
                    elif(time_diff>1):
                        diff = mds_close - prev_mds_close
                        total_mds_close+= (diff/(1000000))
                        prev_mds_close = mds_close
                        
                        
                if "mds_readpage" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_readpage = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_readpage == -1):
                        prev_mds_readpage = mds_readpage
                    elif(time_diff>1):
                        diff = mds_readpage - prev_mds_readpage
                        total_mds_readpage+= (diff/(1000000))
                        prev_mds_readpage = mds_readpage
               
                if "mds_connect" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_connect = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_connect == -1):
                        prev_mds_connect = mds_connect
                    elif(time_diff>1):
                        diff = mds_connect - prev_mds_connect
                        total_mds_connect+= (diff/(1000000))
                        prev_mds_connect = mds_connect
                        
                if "mds_get_root" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_get_root = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_get_root == -1):
                        prev_mds_get_root = mds_get_root
                    elif(time_diff>1):
                        diff = mds_get_root - prev_mds_get_root
                        total_mds_get_root+= (diff/(1000000))
                        prev_mds_get_root = mds_get_root
                        
                if "mds_statfs" in metric_line:
                    tokens = str(metric_line).split(" ")
                    mds_statfs = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and prev_mds_statfs == -1):
                        prev_mds_statfs = mds_statfs
                    elif(time_diff>1):
                        diff = mds_statfs - prev_mds_statfs
                        total_mds_statfs+= (diff/(1000000))
                        prev_mds_statfs = mds_statfs
                        
                if "ldlm_cancel" in metric_line:
                    tokens = str(metric_line).split(" ")
                    ldlm_cancel = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and mds_prev_ldlm_cancel == -1):
                        mds_prev_ldlm_cancel = ldlm_cancel
                    elif(time_diff>1):
                        diff = ldlm_cancel - mds_prev_ldlm_cancel
                        mds_total_ldlm_cancel+= (diff/(1000000))
                        mds_prev_ldlm_cancel = ldlm_cancel
                        
                if "obd_ping" in metric_line:
                    tokens = str(metric_line).split(" ")
                    obd_ping = float(tokens[len(tokens)-2])
                    if (time_diff ==1 and mds_prev_obd_ping == -1):
                        mds_prev_obd_ping = obd_ping
                    elif(time_diff>1):
                        diff = obd_ping - mds_prev_obd_ping
                        mds_total_obd_ping+= (diff/(1000000))
                        mds_prev_obd_ping = obd_ping
            
            proc = Popen(['cat', mdt_path+"/md_stats"], universal_newlines=True, stdout=PIPE)
            res = proc.communicate()[0]
            res_parts = res.split("\n")
            for metric_line in res_parts:
                if "close" in metric_line:
                    tokens = str(metric_line).split(" ")
                    close = float(tokens[len(tokens)-3])
                    if (time_diff == 1 and prev_md_close == -1):
                        prev_md_close = close
                    elif(time_diff>1):
                        diff = close - prev_md_close
                        total_md_close +=diff
                        prev_md_close = close
                
                if "getattr" in metric_line:
                    tokens = str(metric_line).split(" ")
                    getattr_ = float(tokens[len(tokens)-3])
                    if (time_diff == 1 and prev_md_getattr == -1):
                        prev_md_getattr = getattr_
                    elif(time_diff>1):
                        diff = getattr_ - prev_md_getattr
                        total_md_getattr +=diff
                        prev_md_getattr = getattr_
                        
                if "intent_lock" in metric_line:
                    tokens = str(metric_line).split(" ")
                    intent_lock = float(tokens[len(tokens)-3])
                    if (time_diff == 1 and prev_md_intent_lock == -1):
                        prev_md_intent_lock = intent_lock
                    elif(time_diff>1):
                        diff = intent_lock - prev_md_intent_lock
                        total_md_intent_lock +=diff
                        prev_md_intent_lock = intent_lock
                
                if "read_page" in metric_line:
                    tokens = str(metric_line).split(" ")
                    read_page = float(tokens[len(tokens)-3])
                    if (time_diff == 1 and prev_md_read_page == -1):
                        prev_md_read_page = read_page
                    elif(time_diff>1):
                        diff = read_page - prev_md_read_page
                        total_md_readpage +=diff
                        prev_md_read_page = read_page
                
                if "revalidate_lock" in metric_line:
                    tokens = str(metric_line).split(" ")
                    revalidate_lock = float(tokens[len(tokens)-3])
                    if (time_diff == 1 and prev_md_revalidate_lock == -1):
                        prev_md_revalidate_lock = revalidate_lock
                    elif(time_diff>1):
                        diff = revalidate_lock - prev_md_revalidate_lock
                        total_md_revalidate_lock +=diff
                        prev_md_revalidate_lock = revalidate_lock
                
                
    
            if(time_diff>=(.1/sleep_time)):
    
                avg_rto_value = total_rto_value/time_diff
                avg_rtt_value = total_rtt_value/time_diff
                avg_mss_value = total_mss_value/time_diff
                avg_cwnd_value = total_cwnd_value/time_diff
                avg_ssthresh_value = total_ssthresh_value/time_diff
                avg_byte_ack = byte_ack/(1024*1024)
                avg_seg_out = segs_out
                avg_seg_in = segs_in
#                avg_send_value = send/time_diff
                avg_send_value = send
#                p_avg_value = total_pacing_rate/time_diff
                p_avg_value = total_pacing_rate
                avg_unacked_value = unacked
                avg_retrans = retrans/time_diff
                avg_rcv_space = rcv_space/time_diff
                avg_pending_page = total_pending_page/time_diff
                avg_rpc = total_pending_rpc/time_diff
    
    #            print("rtt = "+str(avg_rtt_value)+" pacing_rate = "+str(p_avg_value) + " cwnd = "+str(avg_cwnd_value)+" rto = "+str(avg_rto_value))
    #            print("byte ack = "+str(avg_byte_ack)+" seg out = "+str(avg_seg_out) + " Retrans = "+str(retrans))
    #            print("mss = "+str(avg_mss_value)+" ssthresh = "+str(avg_ssthresh_value) + " seg in = "+str(avg_seg_in))
    #            print("send = "+str(avg_send_value)+" unacked = "+str(avg_unacked_value) + " rcv space = "+str(avg_rcv_space))
    #            
    #            
    #            print("wait time: "+str(total_wait_time)+" req number "+str(total_req_number) + " read bytes "+str(total_read_bytes))
    #            print("ost read: "+str(total_ost_read)+" ost_connect "+str(total_ost_connect) + " ost_statfs "+str(total_ost_statfs))
    #            print("ldlm_cancel: "+str(total_ldlm_cancel)+" obd_ping "+str(total_obd_ping))
    #            
    #            print("mds wait time: "+str(mds_total_req_wait_time)+" mds req number "+str(mds_total_active_req) + " mds_getattr "+str(total_mds_getattr))
    #            print("mds close: "+str(total_mds_close)+" mds read page "+str(total_mds_readpage) + " mds connect "+str(total_mds_connect))
    #            print("mds get root: "+str(total_mds_get_root)+" mds statfs "+str(total_mds_statfs)+" mds ldlm cancel "+str(mds_total_ldlm_cancel))
    #            print("mds obd ping: "+str(mds_total_obd_ping))
    #            
    #            
    #            print("md close: "+str(total_md_close)+" md read page "+str(total_md_readpage) + " mds getattr "+str(total_md_getattr))
    #            print("md intent_lock: "+str(total_md_intent_lock)+" md revalidate_lock "+str(total_md_revalidate_lock))
    #            
    #            print("pending page "+str(avg_pending_page)+" RPC "+str(avg_rpc)+"\n\n")
    #            
                mdt_rpc_avg_waittime, rpc_inflight, rpc_unregistering, rpc_timeouts = process_mds_rpc(mdt_path)
    #            print("rpc avg waitime: "+str(mdt_rpc_avg_waittime)+" rpc_inflight "+str(rpc_inflight) + " rpc_unregistering "+str(rpc_unregistering))
    #            print("rpc_timeouts: "+str(rpc_timeouts))
                
                system_value_list = collect_system_metrics(pid)
    #            print(system_value_list)
                
                
                
                
                
                output_string = str(avg_rtt_value)+","+str(p_avg_value) + ","+str(avg_cwnd_value)+","+str(avg_rto_value)+","+\
                            str(avg_byte_ack)+","+str(avg_seg_out) + ","+str(retrans)+","+\
                            str(avg_mss_value)+","+str(avg_ssthresh_value) + ","+str(avg_seg_in)+","+\
                            str(avg_send_value)+","+str(avg_unacked_value) + ","+str(avg_rcv_space)+","+\
                            str(total_wait_time)+","+str(total_req_number) + ","+str(total_read_bytes)+","+\
                            str(total_ost_read)+","+str(total_ost_connect) + ","+str(total_ost_statfs)+","+\
                            str(total_ldlm_cancel)+","+str(total_obd_ping) +","+\
                            str(mds_total_req_wait_time)+","+str(mds_total_active_req) + ","+str(total_mds_getattr)+","+\
                            str(total_mds_close)+","+str(total_mds_readpage) + ","+str(total_mds_connect)+","+\
                            str(total_mds_get_root)+","+str(total_mds_statfs) + ","+str(mds_total_ldlm_cancel)+","+\
                            str(mds_total_obd_ping)+","+\
                            str(total_md_close)+","+str(total_md_readpage) + ","+str(total_md_getattr)+","+\
                            str(total_md_intent_lock)+","+str(total_md_revalidate_lock)+","+\
                            str(avg_pending_page)+","+str(avg_rpc)+","+\
                            str(mdt_rpc_avg_waittime)+","+str(rpc_inflight) + ","+str(rpc_unregistering)+","+\
                            str(rpc_timeouts)+","+str(send_buffer_value)
                
                global label_value
                for item in system_value_list:
                    output_string+=","+str(item)
                output_string+=","+str(label_value)+"\n"
                main_output_string+=output_string
                
                epoc_count+=1
                if(epoc_count==100):
                    print("tarnsfering file....")
                    epoc_count = 0
                    write_thread =fileWriteThread(main_output_string, label_value)
                    write_thread.start()
                    main_output_string=""
                    
                
                time_diff = 0
                
                total_rto_value, total_rtt_value, total_mss_value, total_cwnd_value, total_ssthresh_value, byte_ack, segs_out, segs_in,\
                send, total_pacing_rate, unacked, retrans, rcv_space = (0,)*13
                
                total_wait_time, total_ost_read, total_req_number, total_read_bytes, total_ost_connect, total_ost_statfs, total_ldlm_cancel,\
                total_obd_ping = (0,)*8
                
                mds_total_req_wait_time, mds_total_active_req, total_mds_getattr, total_mds_close, total_mds_readpage, total_mds_connect,\
                total_mds_get_root, total_mds_statfs, mds_total_ldlm_cancel, mds_total_obd_ping = (0,)*10
        
                total_pending_rpc = 0
                total_pending_page = 0
        except:
            traceback.print_exc()
        time.sleep(sleep_time)

class fileWriteThread(threading.Thread):
    def __init__(self, metric_string, label_value):
        threading.Thread.__init__(self)
        self.metric_string = metric_string
        self.label_value = label_value

    def run(self):
        
        output_string = "avg_rtt_value, p_avg_value ,avg_cwnd_value,avg_rto_value,"+\
                        "avg_byte_ack,avg_seg_out ,retrans,"+\
                        "avg_mss_value,avg_ssthresh_value ,avg_seg_in,"+\
                        "avg_send_value,avg_unacked_value ,avg_rcv_space,"+\
                        "total_wait_time,total_req_number ,total_read_bytes,"+\
                        "total_ost_read,total_ost_connect ,total_ost_statfs,"+\
                        "total_ldlm_cancel,total_obd_ping,"+\
                        "mds_total_req_wait_time,mds_total_active_req ,total_mds_getattr,"+\
                        "total_mds_close,total_mds_readpage ,total_mds_connect,"+\
                        "total_mds_get_root,total_mds_statfs ,mds_total_ldlm_cancel,"+\
                        "mds_total_obd_ping,"+\
                        "total_md_close,total_md_readpage ,total_md_getattr,"+\
                        "total_md_intent_lock,total_md_revalidate_lock,"+\
                        "avg_pending_page,avg_rpc,"+\
                        "mdt_rpc_avg_waittime,rpc_inflight ,rpc_unregistering,"+\
                        "rpc_timeouts,send_buffer_value,label_value\n"
        
        output_file = open("dataset_"+str(self.label_value)+".csv","a+")
        output_file.write(str(self.metric_string))
        output_file.flush()
        output_file.close()

#        if os.path.isfile("dataset.csv"):
#            output_file = open("dataset.csv","a+")
#            output_file.write(str(self.metric_string))
#            output_file.flush()
#            output_file.close()
#        else:
#            output_file = open("dataset.csv","a+")
#            output_file.write(str(output_string))
#            output_file.write(str(self.metric_string))
#            output_file.flush()
#            output_file.close()
        


class statThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        collect_stat()
        

class wholeStatThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        comm_ss = ['python','manager_program_for_file_properties.py']
        proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
        proc.communicate()


class AnomalyThread(threading.Thread):
    def __init__(self, anomaly_type):
        threading.Thread.__init__(self)
        self.type = anomaly_type

    def run(self):
        if(int(self.type)==1):
#            stress --cpu 8 -i 1000 -d 1000 -m 15 --timeout 200s
            comm_ss = ['stress' '-i' '5000']
            proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
            proc.communicate()

#test_thread =testThread()
#test_thread.start()



stat_thread = statThread()
stat_thread.start()

#whole_stat_thread = wholeStatThread()
#whole_stat_thread.start()

#anomaly_thread = AnomalyThread(1)
#anomaly_thread.start()

for x in range(50):
    file_transfer_thread = fileTransferThread(str(x%10))
    file_transfer_thread.start()
    file_transfer_thread.join()

#comm_ss = ['killall' 'stress']
#proc = subprocess.Popen(comm_ss, stdout=subprocess.PIPE)
#proc.communicate()

#
#while(1):
#    background_thread = readbackgroundThread()
#    background_thread.start()
#    background_thread.join()
#print("background thread finished!")
#should_run = False
#sys.exit(0)