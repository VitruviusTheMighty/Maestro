import socket

def client():
  host = '127.0.0.1'  # get local machine name 
  # host = "a machine on your network name"
  port = 7800  # Make sure it's within the > 1024 $$ <65535 range
  
  s = socket.socket()
  s.connect((host, port))
  
  message = input('-> ')
  while message != 'q':
    s.send(message.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print('Received from server: ' + data)
    message = input('==> ')
  s.close()

if __name__ == '__main__':
  client()