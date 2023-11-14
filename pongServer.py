# =================================================================================================
# Contributing Authors:	    Ryan Ennis, Evan Damron
# Email Addresses:          ryan.ennis@uky.edu, evan.damron@uky.edu
# Date:                     11/12/2023
# Purpose:                  Redid while loops
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import time

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

def f1(client1Socket, client2Socket):
    while True:
        try:
            print("f1 FUNCTION TEST")  # debugging reference
            msg = client1Socket.recv(1024)  # receive info from client1

            if not msg:
                print("No message received, client1 may have disconnected.")
                break  # Exit the loop if no message is received

            client2Socket.send(msg)

        except socket.error as e:
            print(f"Socket error occurred: {e}")
            break  # Exit the loop in case of socket error

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Exit the loop in case of any other exception

def handle_client_connection(client_socket):
    try:
        join_message = client_socket.recv(1024).decode()
        if join_message == "JOIN":
            return True
        else:
            client_socket.close()
            return False
    except socket.error:
        client_socket.close()
        return False

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # DGRAM)      # Creating the server
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Working on localhost

    server.bind(("10.47.184.199", 64920))
    server.listen(2)
    print("waiting for client 1...")
    client1_socket, client1_address = server.accept()
    server.settimeout(3)
    ready_to_play = False
    while not ready_to_play:
        try:
            if not handle_client_connection(client1_socket):
                print('waiting for client 1...')
                client1_socket, client1_address = server.accept()
                continue

            client1_socket.send("640,480,left".encode())

            print("waiting for client 2...")
            client2_socket, client2_address = server.accept()
            if not handle_client_connection(client2_socket):
                continue

            print("CLIENT2 JOINED")
            client2_socket.send("640,480,right".encode())


            ready_to_play = True

        except socket.timeout:
            continue

    start_msg = "START"
    client1_socket.send(start_msg.encode())
    client2_socket.send(start_msg.encode())

    thread1 = threading.Thread(target = f1, args = (client1_socket, client2_socket))
    thread2 = threading.Thread(target = f1, args = (client2_socket, client1_socket))

    #Start threads
    thread1.start()
    thread2.start()
    print('made it here1')
    #Wait for threads to each finish
    thread1.join()
    thread2.join()
    print('made it here2')
    client1_socket.close()
    client2_socket.close()
    server.close()