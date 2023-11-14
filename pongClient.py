# =================================================================================================
# Contributing Authors:	    Ryan Ennis, Hunter Brogna, Evan Damron
# Email Addresses:          ryan.ennis@uky.edu, hjbr230@uky.edu, evan.damron@uky.edu
# Date:                     11/12/2023
# Purpose:                  Started planning out encoding/decoding formatting
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import pygame
import tkinter as tk
import sys
import socket

from assets.code.helperCode import *

# This is the main game loop.  For the most part, you will not need to modify this.  The sections
# where you should add to the code are marked.  Feel free to change any part of this project
# to suit your needs.
def playGame(screenWidth:int, screenHeight:int, playerPaddle:str, client:socket.socket) -> None:
    print("playgame!")
    client.settimeout(5)  # timeout after 1 second
    startMsg = ""
    while startMsg != "START":
        try:
            sendMsg = "JOIN"
            client.send(sendMsg.encode())
            print('sent JOIN')
            # Attempt to receive a message
            startMsg = client.recv(1024).decode()
        except socket.timeout:
            continue


    
    # Pygame inits
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    print("playgame 1")

    # Constants
    WHITE = (255,255,255)
    clock = pygame.time.Clock()
    scoreFont = pygame.font.Font("./assets/fonts/pong-score.ttf", 32)
    winFont = pygame.font.Font("./assets/fonts/visitor.ttf", 48)
    pointSound = pygame.mixer.Sound("./assets/sounds/point.wav")
    bounceSound = pygame.mixer.Sound("./assets/sounds/bounce.wav")

    print("playgame 2")

    # Display objects
    print(pygame)
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    winMessage = pygame.Rect(0,0,0,0)
    topWall = pygame.Rect(-10,0,screenWidth+20, 10)
    bottomWall = pygame.Rect(-10, screenHeight-10, screenWidth+20, 10)
    centerLine = []
    for i in range(0, screenHeight, 10):
        centerLine.append(pygame.Rect((screenWidth/2)-5,i,5,5))

    print("playgame 3")

    # Paddle properties and init
    paddleHeight = 50
    paddleWidth = 10
    paddleStartPosY = (screenHeight/2)-(paddleHeight/2)
    leftPaddle = Paddle(pygame.Rect(10,paddleStartPosY, paddleWidth, paddleHeight))
    rightPaddle = Paddle(pygame.Rect(screenWidth-20, paddleStartPosY, paddleWidth, paddleHeight))

    ball = Ball(pygame.Rect(screenWidth/2, screenHeight/2, 5, 5), -5, 0)

    if playerPaddle == "left":
        opponentPaddleObj = rightPaddle
        playerPaddleObj = leftPaddle
    else:
        opponentPaddleObj = leftPaddle
        playerPaddleObj = rightPaddle

    lScore = 0
    rScore = 0

    sync = 0

    print("playgame 4")

    while True:
        # Wiping the screen
        screen.fill((0,0,0))

        # Getting keypress events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    playerPaddleObj.moving = "down"

                elif event.key == pygame.K_UP:
                    playerPaddleObj.moving = "up"

            elif event.type == pygame.KEYUP:
                playerPaddleObj.moving = ""

        print("playgame 5")

        # =========================================================================================
        # Your code here to send an update to the server on your paddle's information,
        # where the ball is and the current score.
        # Feel free to change when the score is updated to suit your needs/requirements
        
        # NOTES FROM RYAN: Things that will probably be encoded and sent to server & decoded and receieved from server
        # 
        # paddle.moving seems to be the info on paddles movement (shocker)
        # lscore and rscore are each players score
        # sync variable will be used to sync up clients when they... get out of sync
        # i dont know exactly what will be used to hold the balls position info
        # END OF RYANS NOTES

        # Client sends encoded message with game info
        sendInfo = playerPaddleObj.moving + "/" + str(lScore) + "/" + str(rScore) + "/" + str(sync) + "/" + \
                   str(ball.rect.x) + "/" + str(ball.rect.y)
        client.send(sendInfo.encode())

        # Client received encoded message from server
        recInfo = client.recv(1024).decode().split("/")
        opponentPaddleObj.moving, rec_lScore_str, rec_rScore_str, rec_sync_str, rec_ball_x_str, rec_ball_y_str = map(str, recInfo)
        rec_lScore, rec_rScore, rec_sync, rec_ball_x, rec_ball_y = int(rec_lScore_str), int(rec_rScore_str), int(rec_sync_str), float(rec_ball_x_str), float(rec_ball_y_str)
        if rec_sync > sync:
            ball.rect.x = rec_ball_x
            ball.rect.y = rec_ball_y
            lScore = rec_lScore
            rScore = rec_rScore
        # =========================================================================================

        # Update the player paddle and opponent paddle's location on the screen
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            if paddle.moving == "down":
                if paddle.rect.bottomleft[1] < screenHeight-10:
                    paddle.rect.y += paddle.speed
            elif paddle.moving == "up":
                if paddle.rect.topleft[1] > 10:
                    paddle.rect.y -= paddle.speed

        # If the game is over, display the win message
        if lScore > 4 or rScore > 4:
            winText = "Player 1 Wins! " if lScore > 4 else "Player 2 Wins! "
            textSurface = winFont.render(winText, False, WHITE, (0,0,0))
            textRect = textSurface.get_rect()
            textRect.center = ((screenWidth/2), screenHeight/2)
            winMessage = screen.blit(textSurface, textRect)
        else:

            # ==== Ball Logic =====================================================================
            ball.updatePos()

            # If the ball makes it past the edge of the screen, update score, etc.
            if ball.rect.x > screenWidth:
                lScore += 1
                pointSound.play()
                ball.reset(nowGoing="left")
            elif ball.rect.x < 0:
                rScore += 1
                pointSound.play()
                ball.reset(nowGoing="right")
                
            # If the ball hits a paddle
            if ball.rect.colliderect(playerPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(playerPaddleObj.rect.center[1])
            elif ball.rect.colliderect(opponentPaddleObj.rect):
                bounceSound.play()
                ball.hitPaddle(opponentPaddleObj.rect.center[1])
                
            # If the ball hits a wall
            if ball.rect.colliderect(topWall) or ball.rect.colliderect(bottomWall):
                bounceSound.play()
                ball.hitWall()
            
            pygame.draw.rect(screen, WHITE, ball)
            # ==== End Ball Logic =================================================================

        # Drawing the dotted line in the center
        for i in centerLine:
            pygame.draw.rect(screen, WHITE, i)
        
        # Drawing the player's new location
        for paddle in [playerPaddleObj, opponentPaddleObj]:
            pygame.draw.rect(screen, WHITE, paddle)

        pygame.draw.rect(screen, WHITE, topWall)
        pygame.draw.rect(screen, WHITE, bottomWall)
        scoreRect = updateScore(lScore, rScore, screen, WHITE, scoreFont)
        pygame.display.update()
        clock.tick(60)
        
        # This number should be synchronized between you and your opponent.  If your number is larger
        # then you are ahead of them in time, if theirs is larger, they are ahead of you, and you need to
        # catch up (use their info)
        sync += 1
        # =========================================================================================
        # Send your server update here at the end of the game loop to sync your game with your
        # opponent's game

        # =========================================================================================




# This is where you will connect to the server to get the info required to call the game loop.  Mainly
# the screen width, height and player paddle (either "left" or "right")
# If you want to hard code the screen's dimensions into the code, that's fine, but you will need to know
# which client is which
def joinServer(ip:str, port:str, errorLabel:tk.Label, app:tk.Tk) -> None:
    try:   # Purpose:      This method is fired when the join button is clicked
        # Arguments:
        # ip            A string holding the IP address of the server
        # port          A string holding the port the server is using
        # errorLabel    A tk label widget, modify it's text to display messages to the user (example below)
        # app           The tk window object, needed to kill the window
        
        # Create a socket and connect to the server
        # You don't have to use SOCK_STREAM, use what you think is best
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#DGRAM)
        client.connect((ip, int(port)))
        # Inform the server that a new client is connecting
        client.send("JOIN".encode())
        print("CLIENT JOIN")    # debugging reference
        server_data = client.recv(1024).decode().split(",")
        print('made it here', server_data)
        screenWidth, screenHeight, playerPaddle = map(str, server_data)
        screenWidth = int(screenWidth)
        screenHeight = int(screenHeight)
        # If you have messages you'd like to show the user use the errorLabel widget like so
        # errorLabel.config(text=f"Connected to the server.\nScreen Width: {screenWidth}, Screen Height: {screenHeight}")
        # You may or may not need to call this, depending on how many times you update the label
        # errorLabel.update()     
        # Close this window and start the game with the info passed to you from the server
        # app.withdraw()     # Hides the window (we'll kill it later)
        playGame(screenWidth, screenHeight, playerPaddle, client)  # User will be either left or right paddle
        app.quit()         # Kills the window
    except ConnectionRefusedError:
        errorLabel.config(text="Connection to the server failed. Please check the IP and Port.")
        errorLabel.update()
    except Exception as e:
        errorLabel.config(text=f"An error occurred: {str(e)}")
        errorLabel.update()


# This displays the opening screen, you don't need to edit this (but may if you like)
def startScreen():
    app = tk.Tk()
    app.title("Server Info")

    image = tk.PhotoImage(file="./assets/images/logo.png")

    titleLabel = tk.Label(image=image)
    titleLabel.grid(column=0, row=0, columnspan=2)

    ipLabel = tk.Label(text="Server IP:")
    ipLabel.grid(column=0, row=1, sticky="W", padx=8)

    ipEntry = tk.Entry(app)
    ipEntry.grid(column=1, row=1)

    portLabel = tk.Label(text="Server Port:")
    portLabel.grid(column=0, row=2, sticky="W", padx=8)

    portEntry = tk.Entry(app)
    portEntry.grid(column=1, row=2)

    errorLabel = tk.Label(text="")
    errorLabel.grid(column=0, row=4, columnspan=2)

    joinButton = tk.Button(text="Join", command=lambda: joinServer(ipEntry.get(), portEntry.get(), errorLabel, app))
    joinButton.grid(column=0, row=3, columnspan=2)

    app.mainloop()

if __name__ == "__main__":
    # startScreen()
    
    # Uncomment the line below if you want to play the game without a server to see how it should work
    # the startScreen() function should call playGame with the arguments given to it by the server this is
    # here for demo purposes only
    # playGame(640, 480,"left",socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    joinServer("10.47.184.199", "64920", tk.Label(text=""), tk.Tk())