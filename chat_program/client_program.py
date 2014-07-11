#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
from threading import _start_new_thread

def clientside(connection):
    while True:
        data=input("User :")
        connection.send(data.encode(encoding='utf_8', errors='strict'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
print(host)
s.connect((host, port))
_start_new_thread(clientside ,(s,))
while True:
    print(s.recv(1024).decode())
s.close                     # Close the socket when done