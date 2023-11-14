# =================================================================================================
# Contributing Authors:	    Ryan Ennis
# Email Addresses:          ryan.ennis@uky.edu
# Date:                     11/12/2023
# Purpose:                  Redid while loops
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games


def f1(client1Socket, client2Socket):
    while True:
        print("f1 FUNCTION TEST")   # debugging reference
        msg = client1Socket.recv(1024)  # receive info from client1
        client2Socket.send(msg)         # send client1 info to client2


def f2(client2Socket, client1Socket):
    while True:
        print("f2 FUNCTION TEST")   # debugging reference
        msg = client2Socket.recv(1024)  # receive info from client2
        client1Socket.send(msg)         # send client2 info to client1

if __name__ == "__main__":

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#DGRAM)      # Creating the server

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost

    server.bind(("localhost", 64920))
    server.listen(2)
    print("test")
    
    # accept client 1 connection
    client1Socket, client1Address = server.accept()

    # Assign playside and default settings to client1
    c1join = ""
    c1join = client1Socket.recv(1024).decode()

    if c1join == "JOIN":
        print("CLIENT1 JOINED") # debugging reference
        c1default = "640,480,left"
        client1Socket.send(c1default.encode())

    # accept client 2 connection
    client2Socket, client2Address = server.accept() 
    
    # Assign playside and default settings to client2
    c2join = ""
    c2join = client2Socket.recv(1024).decode()

    if c2join == "JOIN":
        print("CLIENT2 JOINED") # debugging reference
        c2default = "640,480,right"
        client2Socket.send(c2default.encode())

    thread1 = threading.Thread(target = f1, args = (client1Socket, client2Socket))
    thread2 = threading.Thread(target = f2, args = (client2Socket, client1Socket))

    #Start threads
    thread1.start()
    thread2.start()

    #Wait for threads to each finish
    thread1.join()
    thread2.join()

    client1Socket.close()
    client2Socket.close()
    server.close()