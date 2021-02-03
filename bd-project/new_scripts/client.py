import socket
import threading
import os
import time

import buffer

HOST = '10.52.3.85'
PORT = 50505
BUFFER_SIZE = 4096
time_length = 3600 #one hour data
src_path="/home/cc/to/"
directory = os.listdir(src_path)
start_time = time.time()
for file_ in directory:
    try:
        now = time.time()
        if int(now-start_time)>=time_length:
            is_transfer_done = True
            break

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        filename = os.path.join(src_path, file_)
        s.send(file_+"\n")
        time.sleep(1)
        with open(filename, 'rb') as f:
            while True:
                data = f.read(4096)
                now_inside = time.time()
                if int(now_inside-start_time)>=time_length:
                    break
                if not data:
                    break
                s.send(data)
        print('File Sent ',file_)
        s.close()
    except:
        pass

print(int(now_inside-start_time))