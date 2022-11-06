## An incomplete implementation of a client for the multiplayer
## networked balloon popping game.

import pygame, select
import socket
import os

DIRNAME = os.path.dirname(__file__)

def you_have_a_message (a_socket):
    """
    This function checks whether there is a message waiting to be
    received.
    """

    [in_msgs, out, err] = select.select([a_socket], [], [], 0)
    if len(in_msgs) > 0:
        return True
    else:
        return False

def display_scores(my_win, height, width, font:pygame.font, scores:list):

    index = 0
    # assert len(scores)%2 ==0 # Needs to be an even set of pairs
    if len(scores)%2==0:
        while index < len(scores):
            player = scores[index]
            score = scores[index+1]
            label = font.render(str(player)+"'s Score"+str(score), True, pygame.color.Color("white"))
            my_win.blit(label, (height,width))
            height+=10
            index=index+2


def run_game():

    ## Initialize the pygame submodules and set up the display window.

    pygame.init()

    width = 800
    height = 600
    my_win = pygame.display.set_mode((width,height))

    UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_host = "localhost"
    
    # server_host = "cslab-25.union.edu"
    server_port = 7000
    server_addr = (server_host, server_port)

    mouse_x, mouse_y = 0,0
    ## Load resources
    # dirname = os.path.dirname(__file__)
    image_path = os.path.join(DIRNAME, "red_balloon.gif")

    balloon = pygame.image.load(image_path)
    balloon = balloon.convert()

    wav_path = os.path.join(DIRNAME, "pop.wav")
    pop_sound = pygame.mixer.Sound(wav_path)

    myFont = pygame.font.Font(None,30)

    ## Initialize game objects

    # balloon positions
    b_x = 100
    b_y = 100
    b_xv = 0
    b_yv = 0


    score = 0
    scorelist = []

    name = ""

    clock = pygame.time.Clock()

    ## Initialize loop variables
    intro = True
    keepGoing = True

    #########
    ## The intro screen: lets the player input a name
    #########
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                keepGoing = False

            elif event.type==pygame.KEYDOWN:

                if event.key >= 65 and event.key <= 122:
                    name += chr(event.key)

                if event.key == 13:
                    intro = False

        ## Draw picture and update display
        my_win.fill(pygame.color.Color("darkblue"))

        label = myFont.render("Please enter your name: "+name, True, pygame.color.Color("magenta"))
        my_win.blit(label, (50,height/2-100))

        label = myFont.render("Then hit 'Enter' to start.", True, pygame.color.Color("magenta"))
        my_win.blit(label, (50,height/2-50))

        pygame.display.update()



    ###########
    ## The main game loop: We are using a time based game loop so that
    ## it doesn't matter if the framerate on the server and on the
    ## client computers aren't the same.
    ###########

    ## connect to the server
    msg = "connect "+name
    UDP_sock.sendto(msg.encode('utf-8'), server_addr)

    dt = clock.tick()
    while (keepGoing):

        dt = clock.tick()
        
        ## Handle events.
        
        ## Update game objects

        b_x = b_x + b_xv * dt
        b_y = b_y + b_yv * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print("i clicked at position ", mouse_x, mouse_y)
                click_msg = "click "+str(mouse_x)+" "+str(mouse_y)
                UDP_sock.sendto(click_msg.encode('utf-8'), server_addr)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    print("Hacking - please wait for the balloon to reach its next position before using again")
                    
                    bx = b_x
                    by = b_y
                    if b_xv < 0:
                        bx -=3
                    else:
                        bx +=3
                    
                    if b_yv < 0:
                        by -= 3
                    else:
                        by += 3

                    hack_send = "click "+str(int(bx))+" "+str(int(by))
                    UDP_sock.sendto(hack_send.encode('utf-8'), server_addr)
            

        # handle messages from the server

        # Uncomment the following lines of code. They check whether
        # there is a message from the server waiting and if so,
        # extract the message string and the address of the sender

        if you_have_a_message(UDP_sock):
            received_string, sender = UDP_sock.recvfrom(1024)
            received_string = received_string.decode('utf-8')

            split_recieved = received_string.split(" ")
            # Write code to handle "position" messages
            if "position" in split_recieved:
                # print(split_recieved)
                b_x  = int(split_recieved[1])
                b_y  = int(split_recieved[2])
                # print(f"BX: {b_x}, BY: {b_y}")
                b_xv = float(split_recieved[3])
                b_yv = float(split_recieved[4])     
                
                # hack_send = "click "+str(int(b_x))+" "+str(int(b_y))
                # UDP_sock.sendto(hack_send.encode('utf-8'), server_addr)

                

            # Write code to handle "hit" messages
            elif "hit" in split_recieved:
                score = int(split_recieved[1])
                pop_sound.play()

            elif "miss" in split_recieved:
                score = int(split_recieved[1])

            # Write code to handle "scores" messages
            elif "scores" in split_recieved:
                x = 10
                y = 10
                display_scores(my_win, x,y, myFont, split_recieved[1:-1])
        
            else:
                raise Exception("Did not recognize recieved String!")

        ## Draw picture and update display

        my_win.fill(pygame.color.Color("darkblue"))


        

        # score
        x = 10
        y = 10
        label = myFont.render("Your score: "+str(score), True, pygame.color.Color("magenta"))
        my_win.blit(label, (x,y))



        # Write code to display other player's scores

        # balloon images
        my_win.blit(balloon,(int(b_x), int(b_y)))

        print(f"current_pos: {int(b_x)}, {int(b_y)}, dt: {float(b_xv)}, {float(b_yv)}")
        pygame.display.update()

    ## The game loop ends here. 

    pygame.quit()

    disconnect_message = "disconnect"
    UDP_sock.sendto(disconnect_message.encode('utf-8'), server_addr)



## Call the function run_game.

run_game()
