# import socket
# import os

# import buffer

# HOST = '192.168.1.2'
# PORT = 2345

# # If server and client run in same local directory,
# # need a separate place to store the uploads.
# try:
#     os.mkdir('uploads')
# except FileExistsError:
#     pass

# s = socket.socket()
# s.bind((HOST, PORT))
# s.listen(10)


# while True:
#     conn, addr = s.accept()
#     print("Got a connection from ", addr)
#     connbuf = buffer.Buffer(conn)

#     while True:
#         print("Waiting for a connection.....")
#         file_name = connbuf.get_utf8()
#         if not file_name:
#             break
#         file_name = os.path.join('uploads',file_name)
#         print('file name: ', file_name)

#         file_size = int(connbuf.get_utf8())
#         print('file size: ', file_size )

#         with open(file_name, 'wb') as f:
#             remaining = file_size
#             while remaining:
#                 chunk_size = 4096 if remaining >= 4096 else remaining
#                 chunk = connbuf.get_bytes(chunk_size)
#                 if not chunk: break
#                 f.write(chunk)
#                 remaining -= len(chunk)
#             if remaining:
#                 print('File incomplete.  Missing',remaining,'bytes.')
#             else:
#                 print('File received successfully.')
#     print('Connection closed.')
#     conn.close()


import socket
import threading
import time

serversock = socket.socket()
host = '10.52.3.85'
port = 50505
BUFFER_SIZE = 4096
serversock.bind((host, port))

serversock.listen(10)
print("Waiting for a connection.....")


def reader(client):
    file_name = client.recv(BUFFER_SIZE).decode()
    print(file_name)
    file_name = file_name.strip()
    start_time = time.time()
    byte_received = 0
    output_str="file name: "+file_name+"\n"
    with open(file_name, "wb") as f:
        while True:
            bytes_read = client.recv(BUFFER_SIZE)
            if not bytes_read:    
                f.close()
                print ('file close()')
                break
            # write to the file the bytes we just received
            f.write(bytes_read)
            f.flush()
            byte_received+=len(bytes_read)
            now_inside = time.time()
            if int(now_inside-start_time)>=1:
                # print(time.ctime()," ",byte_received)
                output_str+=str(time.ctime())+" "+str(byte_received)+"\n"
                byte_received=0
                start_time=now_inside

    output_file = open("file_transfer_stat.txt","a+")
    output_file.write(output_str)
    output_file.flush()
    output_file.close()

    # close the client socket
    client.close()


while True:
    client, addr = serversock.accept()
    print("Got a connection from %s" % str(addr))
    client_serve_thread = threading.Thread(target=reader, args=tuple((client,)))
    client_serve_thread.start()
    time.sleep(0.001)

serversock.close()