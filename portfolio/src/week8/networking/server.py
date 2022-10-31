import socket

HOST = "127.0.0.1" 
# PORT = 65432  
PORT = 7800
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # s.bind(('', PORT))
    s.bind((HOST, PORT))

    s.listen()
    print("Listening...\n")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            print("==>" + data.decode('utf-8'))
            if not data:
                break
            conn.sendall(data)