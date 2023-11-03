# =================================================================================================
# Contributing Authors:	    Ryan Ennis
# Email Addresses:          ryan.ennis@uky.edu
# Date:                     11/02/2023
# Purpose:                  laid out threading for clients
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

player1Socket, player1Address = server.accept() # accept player 1 connection
player2Socket, player2Address = server.accept() # accept player 2 connection

def f1(player1Socket):
    test = 0 # does nothing but clears errors

def f2(player2Socket):
    test = 0 # does nothing but clears errors

while True:
    thread1 = threading.Thread(target = f1, args = (player1Socket,))
    thread2 = threading.Thread(target = f2, args = (player2Socket,))

    #Start threads
    thread1.start()
    thread2.start()

    #Wait for threads to each finish
    thread1.join()
    thread2.join()

player1Socket.close()
player2Socket.close()
server.close()