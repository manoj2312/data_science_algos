#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from _multiprocessing import recv
from threading import _start_new_thread

#Function for handling connections. This will be used to create threads
def client_thread(conn):
    welcome_msg='Welcome to the server'
    conn.send(welcome_msg.encode(encoding='utf_8', errors='strict')) 
    while True:
        data = conn.recv(1024)
        reply = data.decode()
        print(reply)
        if not data: 
            break
        for i in client:
            i.sendall(data)
    conn.close()
client = []
global client
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
  
print(host)
s.listen(25)    # Now wait for client connection.

while True:
    c, addr = s.accept()     # Establish connection with client.
    client.append(c)
    print('Got connection from', addr)
    _start_new_thread(client_thread ,(c,))
# s.close()              # Close the connection