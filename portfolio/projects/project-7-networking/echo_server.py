## This is a server for a simple echo application. The server is
## waiting for messages. When it receives a message from a client, it
## simply sends the same message back.

import socket


def run_server():
    # Create a UDP socket
    UDP_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    my_host = ''
    my_port = 7000
    my_addr = (my_host,my_port)

    # set the address under which the server is going to be reachable
    UDP_sock.bind(my_addr)
    print("starting up sever on port", my_port)
    
    # maximum size of messages that can be received
    buffer_size = 1024

    while True:

        print("waiting to receive messages")
        received_string, client = UDP_sock.recvfrom(buffer_size)
        received_string = received_string.decode('utf-8')
        print("received message \""+ received_string+ "\"from client", client)

        print("echoing message back")
        msg = "You said: "  + received_string
        UDP_sock.sendto(msg.encode('utf-8'), client)
        

run_server()
