import socket

# Create a UDP socket
UDP_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ("cslab-25.union.edu", 7000)

# maximum size of messages that can be received
buffer_size = 1024

# Send data
print("sending message")
message = input("==> ")
# while True:
# message = "ello govnah!"
UDP_sock.sendto(message.encode('utf-8'), server_address)

# Receive response
print("waiting to receive response")
response_string, server = UDP_sock.recvfrom(buffer_size)
response_string = response_string.decode('utf-8')
print("response is:", response_string)

# closing socket
UDP_sock.close()


