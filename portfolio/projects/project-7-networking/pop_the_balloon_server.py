
import pygame, random
from socket import *
import select
import os

def clicked_image(mouse_x, mouse_y, x, y, w, h):

    if mouse_x >= x and mouse_x <= x+w and mouse_y >= y and mouse_y <= y+h:
        return True
    else:
        return False


def make_scores_msg (client_d):

    string = "scores"
    for (name, score) in client_d.values():
        string = string + " "+name+ ":" +str(score)

    return string


def move_and_bounce_object(dt, x, y, speed_x, speed_y, obj_width, obj_height, width, height):
    """
    This function calculates an object's new position based on its
    old position, the time that has passed since the last update,
    and its speed. It also makes sure that the object bounces
    off the edge of the screen.
    """

    x = x + dt * speed_x
    if (x < 0):
        x = 0
        speed_x = - speed_x
    elif (x > width - obj_width):
        x = width - obj_width
        speed_x = - speed_x
        
    y = y + dt * speed_y
    if (y < 0):
        y = 0
        speed_y = - speed_y
    elif (y > height - obj_height):
        y = height - obj_height
        speed_y = - speed_y

    return x, y, speed_x, speed_y



def run_game():

    pygame.init()

    my_host = ''
    my_port = 7000
    my_addr = (my_host,my_port)
    buf = 1024
    UDP_sock = socket(AF_INET,SOCK_DGRAM)
    UDP_sock.bind(my_addr)
    print("server started up on port", my_port)

    width = 800
    height = 600

    dirname = os.path.dirname(__file__)
    image_path = os.path.join(dirname, "red_balloon.gif")

    balloon = pygame.image.load(image_path)


    # initialize the balloons' positions and speeds
    b_x = 100
    b_y = 100
    b_speed_x = 0.2
    b_speed_y = 0.2
    b_w = balloon.get_width()
    b_h = balloon.get_height()

    client_d = {}

    score = 0

    clock = pygame.time.Clock()
    num = 0

    timer = 0

    keepGoing = True


    while (keepGoing):

        dt = clock.tick(60)
        timer += dt

        # handle messages from the clients

        # really this should be in its own method, right?
        # grab any messages
        [in_msgs, out, err] = select.select([UDP_sock], [], [], 0)
        if len(in_msgs) > 0:
            #receive and decode message
            received_string, client = UDP_sock.recvfrom(buf)
            received_string = received_string.decode('utf-8')
            received_string = received_string.strip()
            if client in client_d:
                print("I received the following message from",client_d[client][0],":", received_string)
            else:
                print("I received the following message from",client,":", received_string)
            
            received_list = received_string.split(" ")


            if len(received_list) > 0:
                if received_list[0] == "click" and len(received_list) >= 3:

                    if clicked_image (int(received_list[1]), int(received_list[2]), b_x, b_y, b_w, b_h):
                        
                        client_d[client] = (client_d[client][0], client_d[client][1] + 1)
                        msg = "hit "+str(client_d[client][1])
                        msg = msg.encode('utf-8')
                        UDP_sock.sendto(msg, client)
                        b_x = random.randint(0,width)
                        b_y = random.randint(0,height)

                    else:
                        client_d[client] = (client_d[client][0], client_d[client][1] - 1)
                        UDP_sock.sendto("hit "+str(client_d[client][1]), client)
                    
                elif received_list[0] == "connect" and len(received_list) >= 2:
                    name = received_list[1]
                    print("new connection from "+name+" at "+str(client))
                    client_d[client] = (name,0)

                elif received_list[0] == "disconnect":
                    if client in client_d:
                        print(client_d[client][0] + " has disconnected")
                        del client_d[client]
                

        # Update the positions and speeds of the balloons.        
        b_x, b_y, b_speed_x, b_speed_y = move_and_bounce_object(dt, b_x, b_y, b_speed_x, b_speed_y, b_w, b_h, width, height)


        pos = "position "+str(int(b_x))+" "+str(int(b_y))+" "+str(float(b_speed_x))+" "+str(float(b_speed_y))+" "+str(num)
        scores = make_scores_msg(client_d)

        if timer > 90:
            for addr in client_d.keys():
                UDP_sock.sendto(pos.encode('utf-8'), addr)
                UDP_sock.sendto(scores.encode('utf-8'), addr)
            timer = 0

    pygame.quit()
            
 
run_game()
