# =================================================================================================
# Contributing Authors:	    Ryan Ennis
# Email Addresses:          ryan.ennis@uky.edu
# Date:                     10/31/2023 halloween yippee
# Purpose:                  start server socket stuff
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

server.bind(("localhost", 12321))
server.listen(2)

player1Socket, player1Address = server.accept() # accept player 1 connection
player2Socket, player2Address = server.accept() # accept player 2 connection