# =================================================================================================

# Contributing Authors:	    Ryan Ennis, Evan Damron
# Email Addresses:          ryan.ennis@uky.edu, evan.damron@uky.edu
# Date:                     11/15/2023
# Purpose:                  Completed Code

# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import select
import threading
import time

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games


def flushSocket(socket) -> None:    # Clears the sockets buffer
    # Author:       Evan Damron
    # Purpose:      This function aids in clearing the buffers for the socket
    # Pre:          The socket has to be established beforehand
    # Post:         The socket buffers will be clear
    socket.setblocking(0)  # Set socket to non-blocking mode
    try:
        while True:  # Attempt to read continuously until no more data
            data = socket.recv(1024)  # Adjust buffer size as needed
            if not data:
                break  # If no data is received, exit the loop
    except BlockingIOError:
        pass  # There's no more data to read
    socket.setblocking(1)  #set socket back to blocking mode

def f1(receivingSocket, sendingSocket) -> None:     # Relay game info between clients
    # Author:       Ryan Ennis, Evan Damron
    # Purpose:      This function allows the game info from each client to be relayed between the two clients
    # Pre:          The two clients have to be established and playing the game
    # Post:         While playing the game, the info will be relayed between the two clients
    print("The game is running")
    flushSocket(receivingSocket)

    while True:
        try:
            msg = receivingSocket.recv(1024)  # receive info from client1
            if not msg:
                print("No message received, client may have disconnected.")
                break  # Exit the loop if no message is received
            sendingSocket.send(msg)
        except socket.error as e:                   # Send sync = -1 when a client has disconnected or ran into error
            print(f"Socket error occurred: {e}")
            sendInfo = "0/0/0/-1/0/0"
            sendingSocket.send(sendInfo.encode())
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sendInfo = "0/0/0/-1/0/0"
            sendingSocket.send(sendInfo.encode())
            break  # Exit the loop in case of any other exception

def clientStillHere(client_socket) -> bool:     # Checks if client1 is still present prior to client2's connection
    # Author:       Evan Damron
    # Purpose:      This function allows the players to know if both of the clients are still present and connected to the server
    # Pre:          Both clients have to be established and connected
    # Post:         During the game, if a player is disconnected, the game will stop and tell the other client
    try:
        client_socket.settimeout(.5)
        messages = client_socket.recv(1024).decode()
        message = messages.split("/")[-1]
        client_socket.settimeout(None)

        if message == "HERE":       # client1 is present
            return True
        else:                       # client1 is not present
            client_socket.close()
            return False
    except socket.error:            # client1 has stopped responding, disconnect
        client_socket.close()
        return False

if __name__ == "__main__":
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost

        server.bind(("10.47.184.199", 64920))
        server.listen(2)

        print("Waiting for client 1...")
        # Connect client1 and assign game info
        client1_socket, client1_address = server.accept()
        client1_socket.send("640,480,left".encode())
        print('Client 1 connected, waiting for client 2...')

        # Server will stay running even after game has finished
        while True:
            # check if client 1 is still connected
            if clientStillHere(client1_socket):
                # Use select to wait for 3 seconds for a client to connect
                readable, _, _ = select.select([server], [], [], 0)
                if readable:  # If the list is not empty, a client is ready to connect
                    # Connect client2 and assign game info
                    client2_socket, client2_address = server.accept()
                    client2_socket.send("640,480,right".encode())
                    break
            else:
                print("client 1 disconnected... attempting to reconnect")
                client1_socket, client1_address = server.accept()
                client1_socket.send("640,480,left".encode())
                print('reconnected!')
        server.settimeout(None)

        # Both clients have connected, tell client1 to start game (client2 is already starting)
        start_msg = "START"
        client1_socket.send(start_msg.encode())

        thread1 = threading.Thread(target = f1, args = (client1_socket, client2_socket))
        thread2 = threading.Thread(target = f1, args = (client2_socket, client1_socket))

        #Start threads
        thread1.start()
        thread2.start()
        #Wait for threads to each finish
        thread1.join()
        thread2.join()
        print('threads have finished')
        time.sleep(5)
        client1_socket.close()
        client2_socket.close()
        server.close()

