import socket
from threading import Thread
import os

TCP_IP = '192.168.1.2'
TCP_PORT = 60001
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

print ('TCP_IP=',TCP_IP)
print ('TCP_PORT=',TCP_PORT)

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))

    def run(self):
        received = self.sock.recv(BUFFER_SIZE).decode()
        print(received)
        filename, filesize = received.split(SEPARATOR)
        print(filename)
        print(filesize)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)

        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = self.sock.recv(BUFFER_SIZE)
                if not bytes_read:    
                    f.close()
                    print ('file close()')
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                f.flush()

        # close the client socket
        self.sock.close()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))


while True:
    threads = []
    tcpsock.listen(1000)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from ', (ip,port))
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

    for t in threads:
        t.join()