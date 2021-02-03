import socket
import time
import os

#TCP_IP = 'localhost'
TCP_IP = '192.168.1.2'
TCP_PORT = 60001
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024
src_path="/data/masud/STransfer1/to/"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
for i in range(3):

    filename = src_path+str(i)
    # get the file size
    filesize = os.path.getsize(filename)
    s.send(f"filename {str(i)}{SEPARATOR}{filesize}".encode())
    time.sleep(3)

    clock_start = time.clock()
    time_start = time.time()

    with open(filename, 'rb') as f:
        print ('file opened')
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

    print('Successfully get the file')
    s.close()
    print('connection closed')

    clock_end = time.clock()
    time_end = time.time()

# duration_clock = clock_end - clock_start
# print ('clock:  start = ',clock_start, ' end = ',clock_end
# print ('clock:  duration_clock = ', duration_clock

# duration_time = time_end - time_start
# print 'time:  start = ',time_start, ' end = ',time_end
# print 'time:  duration_time = ', duration_time