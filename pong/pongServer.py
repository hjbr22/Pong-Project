# =================================================================================================
# Contributing Authors:	    Ryan Ennis
# Email Addresses:          ryan.ennis@uky.edu
# Date:                     11/05/2023
# Purpose:                  Completed thread functions
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost

server.bind(("localhost", 64920))
server.listen(2)

client1Socket, client1Address = server.accept() # accept client 1 connection
client2Socket, client2Address = server.accept() # accept client 2 connection

def f1(client1Socket, client2Socket):
    msg = ""
    msg = client1Socket.recv(1024)  # receive info from client1
    client2Socket.send(msg)         # send client1 info to client2


def f2(client2Socket, client1Socket):
    msg = ""
    msg = client2Socket.recv(1024)  # receive info from client1
    client1Socket.send(msg)         # send client1 info to client2

while True:
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