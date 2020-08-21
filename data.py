
import os.path
import sys
import numpy as np
import time

label = 0
label_column = 0

def write_to(output):
    with open("data.csv",'a+') as output_file:
        output_file.write(output)

def read_in(filename1, filename2, filename3, filename4,data_amount):
    print(filename1,filename2,filename3,filename4)
    label = 0
    data_pt = 0
    
    file_1 = open(filename1, 'rt') #CPU files
    file_2 = open(filename2, 'rt') #IO files
    file_3 = open(filename3, 'rt') #Mem files
    file_4 = open(filename4, 'rt') #Net files
    
    line1 = file_1.readline()
    line2 = file_2.readline()
    line3 = file_3.readline()
    line4 = file_4.readline()
    #print(filename1)
    FLAG = 1
    break_flag = 0
    while True:
        arr = ''
        data_pt_1 = -1
        data_pt_2 = -1
        data_pt_3 = -1
        data_pt_4 = -1
        #CPU metrics

        if len(line1) <= 1 or line1 == "":
            # read in next line
            line1 = file_1.readline()
        
        elif "Running" in line1:
            index1 = line1.find(":")
            label = int(line1[index1+1:])
            #read in next line
            line1 = file_1.readline()
            if label == 30:
                FLAG = 0
        
        #if ("Data" in line1) or ("Data" in line2) or ("Data" in line3) or ("Data" in line4):
        elif "Data" in line1:
            index1_1 = line1.find("pt ")
            index2_1 = line1.find(":")
            data_pt_1 = int(line1[index1_1+3:index2_1])
            #read in next line
            line1 = file_1.readline()
            if data_pt_1 == data_amount-1 and FLAG == 0:
                break_flag = 1
        
        if data_pt_1 != -1:
            while data_pt_2 != data_pt_1:
                if len(line2) <= 1 or line2 == "" or "Running" in line2:
                    line2 = file_2.readline()
                elif "Data" in line2:
                    index1_2 = line2.find("pt ")
                    index2_2 = line2.find(":")
                    data_pt_2 = int(line2[index1_2+3:index2_2])
                    line2 = file_2.readline()
            
            while data_pt_3 != data_pt_1:
                if len(line3) <= 1 or line3 == "" or "Running" in line3:
                    line3 = file_3.readline()
                elif "Data" in line3:
                    index1_3 = line3.find("pt ")
                    index2_3 = line3.find(":")
                    data_pt_3 = int(line3[index1_3+3:index2_3])
                    line3 = file_3.readline()
            
            while data_pt_4 != data_pt_1:
                if len(line4) <= 1 or line4 == "" or "Running" in line4:
                    line4 = file_4.readline()
                elif "Data" in line4:
                    index1_4 = line4.find("pt ")
                    index2_4 = line4.find(":")
                    data_pt_4 = int(line4[index1_4+3:index2_4])
                    line4 = file_4.readline()
        

            data_pt = data_pt_1
            arr += str(label) + ","
            #print(len(line),line)
            #---------------------------CPU METRICS---------------------------
            info1_1 = line1.split("--->")
            info2_1 = info1_1[1].split(" | ")
            #for each item in the line
            for index in info2_1:
                # only taking the changing variables
                if "User" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "System %" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Idle" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Percent" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Frequency" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","

            #---------------------------IO METRICS---------------------------
            info1_2 = line2.split("--->")
            info2_2 = info1_2[1].split(" | ")
            #for each item in the line
            for index in info2_2:
                # only taking the changing variables
                if "Read Count:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Read Bytes:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Read Times:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Read Merge:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Write Count:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Write Bytes:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Write Times:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Write Merge:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Busy Times:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "r/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "w/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "rkB/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "wkB/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "rrqm/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "wrqm/s:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "rrqm:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "wrqm:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "r_await:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "w_await:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "aqu-sz:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "rareq-sz:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "wareq-sz:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "util:" in index:
                    #print(index)
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:-4])) + ","
            
            #---------------------------MEM METRICS---------------------------
            info1_3 = line3.split("--->")
            info2_3 = info1_3[1].split(" | ")

            for index in info2_3:
                if "Total:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Available:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Percent:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Used:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Free:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Active:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Inactive:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Buffers:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Cached:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
                elif "Slab:" in index:
                    index2 = index.find(":")
                    arr += str(float(index[index2+1:])) + ","
            
            #---------------------------NET METRICS---------------------------
            info1_4 = line4.split("--->")
            info2_4 = info1_4[1].split(" | ")
            array = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
            
            for index in range(len(info2_4)):
                if "Bytes Sent:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[0] += float(info2_4[index][index2+2:])
                elif "Bytes Received:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[1] += float(info2_4[index][index2+2:])
                elif "Packets Sent:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[2] += float(info2_4[index][index2+2:])
                elif "Packets Received:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[3] += float(info2_4[index][index2+2:])
                elif "Errors In:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[4] += float(info2_4[index][index2+2:])
                elif "Errors Out:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[5] += float(info2_4[index][index2+2:])
                elif "Drop In:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[6] += float(info2_4[index][index2+2:])
                elif "Drop Out:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[7] += float(info2_4[index][index2+2:])
                elif "rto:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[8] += float(info2_4[index][index2+1:])
                elif "rtt:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[9] += float(info2_4[index][index2+1:])
                elif "mss:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[10] += float(info2_4[index][index2+1:])
                elif "cwnd:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[11] += float(info2_4[index][index2+1:])
                elif "ssthresh:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[12] += float(info2_4[index][index2+1:])
                elif "bytes_acked:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[13] += float(info2_4[index][index2+1:])
                elif "segs_out:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[14] += float(info2_4[index][index2+1:])
                elif "segs_in:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[15] += float(info2_4[index][index2+1:])
                elif "send" in info2_4[index]:
                    index2 = info2_4[index].find("Mbps")
                    array[16] += float(info2_4[index][4:index2])
                elif "pacing_rate" in info2_4[index]:
                    index2 = info2_4[index].find("Mbps")
                    array[17] += float(info2_4[index][11:index2])
                elif "unacked:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[18] += float(info2_4[index][index2+1:])
                elif "retrans:" in info2_4[index]:
                    index2 = info2_4[index].find("/")
                    array[19] += float(info2_4[index][8:index2])
                    if "lost:" in info2_4[index]:
                        index_ = info2_4[index].find("l")
                        index3 = info2_4[index].find("t:")
                        array[20] += float(info2_4[index][index2+1:index_])
                        array[21] += float(info2_4[index][index3+2:])
                    elif "reordering:" in info2_4[index]:
                        index_ = info2_4[index].find("reo")
                        index3 = info2_4[index].find("g:")
                        array[20] += float(info2_4[index][index2+1:index_])
                        array[22] += float(info2_4[index][index3+2:])
                    elif "rcv_space:" in info2_4[index]:
                        index_ = info2_4[index].find("rcv")
                        array[20] += float(info2_4[index][index2+1:index_])
                    elif "sacked:" in info2_4[index]:
                        index_ = info2_4[index].find("sa")
                        index3 = info2_4[index].find("d:")
                        array[20] += float(info2_4[index][index2+1:index_])
                        array[23] += float(info2_4[index][index3+2:])
                    else:
                        array[20] += float(info2_4[index][index2+1:])
                elif "rcv_space:" in info2_4[index]:
                    index2 = info2_4[index].find(":")
                    array[24] += float(info2_4[index][index2+1:])
            
            for ele in range(len(array)):
                if ele == len(array)-1:
                    arr += str(array[ele]) + "\n"
                else:
                    arr += str(array[ele]) + ","
            
            write_to(arr)

            line1 = file_1.readline()
            line2 = file_2.readline()
            line3 = file_3.readline()
            line4 = file_4.readline()
        
        if break_flag == 1:
            break
    file_1.close()
    file_2.close()
    file_3.close()
    file_4.close()
    #print(arr)

#arr = 'label,CPU user%,CPU system%,CPU idle%,CPU percent,CPU frequency,Read Count,Read Bytes,Read Times,Read Merge,Write Count,Write Bytes,Write Times,Write Merge,Busy Times,r/s,w/s,rkB/s,wkB/s,rrqm/s,rrqm,wrqm,r_await,w_await,aqu-sz,rareq-sz,wareq-sz,util%,Total,Available,Memory Percent,Used,Free,Active,Inactive,Buffers,Cached,Shared,Slab,Bytes Sent,Bytes Received,Packets Sent,Packets Received,Errors In,Errors Out,Drop In,Drop Out,rto,rtt,mss,cwnd,ssthresh,bytes_acked,segs_out,segs_in,send,pacing_rate,unacked,retrans,lost,reordering,sacked,rcv_space\n'
#write_to(arr)  
read_in("stats/cpu_metrics_1.txt","stats/io_metrics_1.txt","stats/mem_metrics_1.txt","stats/net_metrics_1.txt",300)
read_in("stats/cpu_metrics_2.txt","stats/io_metrics_2.txt","stats/mem_metrics_2.txt","stats/net_metrics_2.txt",600)
read_in("stats/cpu_metrics_ld_1.txt","stats/io_metrics_ld_1.txt","stats/mem_metrics_ld_1.txt","stats/net_metrics_ld_1.txt",600)
read_in("stats/cpu_metrics_ld_2.txt","stats/io_metrics_ld_2.txt","stats/mem_metrics_ld_2.txt","stats/net_metrics_ld_2.txt",600)
read_in("stats/cpu_metrics_ld_3.txt","stats/io_metrics_ld_3.txt","stats/mem_metrics_ld_3.txt","stats/net_metrics_ld_3.txt",600)
